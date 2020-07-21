import os


def install_lib(library_list):
    """
    安装库
    :param library_list:
    :return:
    """
    for lib in library_list:
        os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple " + lib)


def upgrade_lib(upgrade_list):
    """
    更新库
    :param upgrade_list:
    :return:
    """
    for lib in upgrade_list:
        os.system("pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple " + lib)


if __name__ == '__main__':
    library_install_list = ['scrapy', 'wheel', 'Twisted']
    library_upgrade_list = []
    install_lib(library_install_list)
    upgrade_lib(library_upgrade_list)
