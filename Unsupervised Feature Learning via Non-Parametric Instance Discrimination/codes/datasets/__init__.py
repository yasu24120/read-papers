from .folder import ImageFolderInstance
from .cifar import CIFAR10Instance, CIFAR100Instance
from .mnist import MNISTInstance
from .folder_custom import ImageFolder

__all__ = ('ImageFolderInstance', 'MNISTInstance', 'CIFAR10Instance', 'CIFAR100Instance', 'ImageFolder',  'DatasetFolder')

