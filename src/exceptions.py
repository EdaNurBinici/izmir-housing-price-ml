"""
Özel exception sınıfları
"""


class ProjectException(Exception):
    """Proje için temel exception sınıfı"""
    pass


class ModelLoadError(ProjectException):
    """Model yükleme hatası"""
    pass


class DataLoadError(ProjectException):
    """Veri yükleme hatası"""
    pass


class PredictionError(ProjectException):
    """Tahmin hatası"""
    pass


class ConfigError(ProjectException):
    """Config hatası"""
    pass


class ValidationError(ProjectException):
    """Veri doğrulama hatası"""
    pass
