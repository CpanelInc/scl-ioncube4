OBS_PROJECT := EA4
scl-php56-php-ioncube4-obs : DISABLE_BUILD += repository=CentOS_8
scl-php55-php-ioncube4-obs : DISABLE_BUILD += repository=CentOS_8
scl-php54-php-ioncube4-obs : DISABLE_BUILD += repository=CentOS_8
OBS_PACKAGE := scl-ioncube
include $(EATOOLS_BUILD_DIR)obs-scl.mk