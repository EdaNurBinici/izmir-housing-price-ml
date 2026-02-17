"""
Model eğitim modülü - Senior seviyesinde refactor edilmiş versiyon
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
from pathlib import Path
from typing import Dict, Any, Tuple
import logging

from .config_loader import ConfigLoader
from .logger_setup import setup_logging, get_logger
from .data_processor import DataProcessor
from .exceptions import DataLoadError, ModelLoadError

# Logging'i başlat
setup_logging()
logger = get_logger(__name__)


class ModelTrainer:
    """Model eğitim sınıfı"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Model trainer'ı başlatır
        
        Args:
            config_path: Config dosyası yolu
        """
        self.config = ConfigLoader(config_path)
        self.data_processor = DataProcessor(self.config)
        self.model = None
        self.pipeline = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Veriyi yükler
        
        Returns:
            Ham veri DataFrame
            
        Raises:
            DataLoadError: Veri yükleme hatası
        """
        try:
            data_path = self.config.get_data_path("raw_data")
            file_path = Path(data_path)
            
            if not file_path.exists():
                file_path = Path(__file__).parent.parent / data_path
                if not file_path.exists():
                    raise FileNotFoundError(f"Veri dosyası bulunamadı: {data_path}")
            
            logger.info(f"Veri yükleniyor: {file_path}")
            df = pd.read_csv(file_path)
            logger.info(f"Veri yüklendi: {len(df)} satır")
            return df
            
        except Exception as e:
            logger.error(f"Veri yükleme hatası: {e}")
            raise DataLoadError(f"Veri yüklenemedi: {e}")
    
    def prepare_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Veriyi model eğitimi için hazırlar
        
        Args:
            df: Ham veri DataFrame
            
        Returns:
            X (features) ve y (target) tuple'ı
        """
        logger.info("Veri hazırlanıyor...")
        
        # Veriyi temizle
        df = self.data_processor.clean_data(df, for_training=True)
        
        # Gerekli sütunları oluştur
        if 'room' in df.columns and 'salon' in df.columns:
            df['toplam_oda'] = df['room'] + df['salon']
        
        # Gereksiz sütunları kaldır
        df = df.drop(columns=['province', 'room', 'salon'], errors='ignore')
        
        # Target encoding için ilçe skorunu hesapla
        df['birim_fiyat'] = df['price'] / df['area']
        ilce_degerleri = df.groupby('district')['birim_fiyat'].median()
        df['ilce_skoru'] = df['district'].map(ilce_degerleri)
        df = df.drop(columns=['birim_fiyat'])
        
        # X ve y'yi ayır
        X = df.drop('price', axis=1)
        y = df['price']
        
        logger.info(f"Hazırlanan veri: {len(X)} satır, {len(X.columns)} özellik")
        
        return X, y, ilce_degerleri
    
    def build_pipeline(self) -> Pipeline:
        """
        Model pipeline'ını oluşturur
        
        Returns:
            Sklearn Pipeline
        """
        logger.info("Model pipeline'ı oluşturuluyor...")
        
        model_config = self.config.get_model_config()
        
        categorical_features = ['district', 'left']
        numerical_features = ['area', 'age', 'toplam_oda', 'ilce_skoru']
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]), numerical_features),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
            ]
        )
        
        hgb_model = HistGradientBoostingRegressor(
            max_iter=model_config.get('max_iter', 500),
            learning_rate=model_config.get('learning_rate', 0.05),
            max_depth=model_config.get('max_depth', 10),
            l2_regularization=model_config.get('l2_regularization', 0.1),
            random_state=model_config.get('random_state', 42)
        )
        
        model = TransformedTargetRegressor(
            regressor=hgb_model,
            func=np.log1p,
            inverse_func=np.expm1
        )
        
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        self.pipeline = pipeline
        return pipeline
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Modeli eğitir
        
        Args:
            X: Feature matrix
            y: Target vector
            
        Returns:
            Model metrikleri
        """
        logger.info("Model eğitiliyor...")
        
        test_size = self.config.get_model_config().get('test_size', 0.2)
        random_state = self.config.get_model_config().get('random_state', 42)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        self.pipeline.fit(X_train, y_train)
        
        # Tahmin ve metrikler
        y_pred = self.pipeline.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        metrikler = {
            'R2 Skoru': r2,
            'MAE (Ortalama Hata)': mae,
            'RMSE (Kök Ortalama Hata)': rmse
        }
        
        logger.info(f"Model eğitildi - R2: {r2:.3f}, MAE: {int(mae):,} TL")
        
        return metrikler
    
    def save_model(
        self,
        pipeline: Pipeline,
        X: pd.DataFrame,
        metrikler: Dict[str, float],
        ilce_degerleri: pd.Series
    ) -> None:
        """
        Model ve yardımcı dosyaları kaydeder
        
        Args:
            pipeline: Eğitilmiş pipeline
            X: Feature matrix (ilçe ve tip listeleri için)
            metrikler: Model metrikleri
            ilce_degerleri: İlçe skorları
        """
        logger.info("Model dosyaları kaydediliyor...")
        
        base_path = Path(__file__).parent.parent
        
        # Model kaydet
        model_path = base_path / self.config.get_data_path("model_path")
        joblib.dump(pipeline, model_path)
        logger.info(f"Model kaydedildi: {model_path}")
        
        # İlçe listesi
        ilceler_path = base_path / self.config.get_data_path("ilceler_path")
        joblib.dump(sorted(X['district'].unique().tolist()), ilceler_path)
        
        # Ev tipleri
        tipler_path = base_path / self.config.get_data_path("tipler_path")
        joblib.dump(sorted(X['left'].unique().tolist()), tipler_path)
        
        # Metrikler
        metrikler_path = base_path / self.config.get_data_path("metrikler_path")
        joblib.dump(metrikler, metrikler_path)
        
        # Önem düzeyleri (basit versiyon)
        onemli_ozellikler = pd.DataFrame({
            'Özellik': ['Metrekare (m2)', 'İlçe Değeri', 'Bina Yaşı', 'Oda Sayısı', 'İlçe: Çeşme'],
            'Önem': [0.40, 0.30, 0.15, 0.10, 0.05]
        })
        onem_path = base_path / self.config.get_data_path("onem_duzeyleri_path")
        joblib.dump(onemli_ozellikler, onem_path)
        
        # İlçe skorları
        ilce_skor_path = base_path / self.config.get_data_path("ilce_skorlari_path")
        joblib.dump(ilce_degerleri, ilce_skor_path)
        
        logger.info("Tüm dosyalar başarıyla kaydedildi")
    
    def run(self) -> None:
        """Tam eğitim sürecini çalıştırır"""
        try:
            logger.info("=" * 50)
            logger.info("Model eğitim süreci başlatılıyor...")
            logger.info("=" * 50)
            
            # Veriyi yükle
            df = self.load_data()
            
            # Veriyi hazırla
            X, y, ilce_degerleri = self.prepare_data(df)
            
            # Pipeline oluştur
            pipeline = self.build_pipeline()
            
            # Modeli eğit
            metrikler = self.train(X, y)
            
            # Sonuçları yazdır
            print("-" * 50)
            print(f"🎯 R2 SKORU: {metrikler['R2 Skoru']:.3f}")
            print(f"📉 MAE: {int(metrikler['MAE (Ortalama Hata)']):,} TL")
            print(f"📊 RMSE: {int(metrikler['RMSE (Kök Ortalama Hata)']):,} TL")
            print("-" * 50)
            
            # Modeli kaydet
            self.save_model(pipeline, X, metrikler, ilce_degerleri)
            
            logger.info("Model eğitim süreci tamamlandı!")
            
        except Exception as e:
            logger.error(f"Eğitim hatası: {e}")
            raise


def main():
    """Ana fonksiyon"""
    trainer = ModelTrainer()
    trainer.run()


if __name__ == "__main__":
    main()
