# -*- coding:utf-8 -*-

#############################################################################
import os

#############################################################################
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UTIL = os.path.join(BASE_DIR, "util")
TMP = os.path.join(BASE_DIR, "tmp")

IN = os.path.join(TMP, "in")
OUT = os.path.join(TMP, "out")

#############################################################################
APK_TOOL = os.path.join(UTIL, "apktool_2.4.1.jar")

SIGN_KEY_JAR = os.path.join(UTIL, "signapk")
signapk = os.path.join(SIGN_KEY_JAR, "signapk.jar")
certificate = os.path.join(SIGN_KEY_JAR, "certificate.pem")
pk8 = os.path.join(SIGN_KEY_JAR, "key.pk8")

#############################################################################
DECODE_DIR = os.path.join(TMP, "decode")

MANIFEST = os.path.join(DECODE_DIR, r"AndroidManifest.xml")
MANIFEST_WRITE = os.path.join(DECODE_DIR, r"AndroidManifest_tmp.xml")

OUT_APK = os.path.join(OUT, "out.apk")
