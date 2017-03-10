#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

"""
Gmail
Gmailで簡単にメール送信
"""

import os.path
import datetime
import smtplib
from email import Encoders
from email.Utils import formatdate
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from credentials import GMAIL_ADDR, GMAIL_PW

# Gmailアカウント
#ADDRESS = "Gmailのアドレス"
#PASSWARD = "Gmailのパスワード"

# SMTPサーバの設定(Gmail用)
SMTP = "smtp.gmail.com"
PORT = 587


def create_message(from_addr, to_addr, subject, body, mime=None, attach_file=None):
    """
    メッセージを作成する
    @:param from_addr 差出人
    @:param to_addr 宛先
    @:param subject 件名
    @:param body 本文
    @:param mime MIME
    @:param attach_file 添付ファイル
    @:return メッセージ
    """
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = formatdate()
    msg["Subject"] = subject
    body = MIMEText(body.encode('utf-8'))
    msg.attach(body)

    # 添付ファイル
    if mime != None and attach_file != None:
        attachment = MIMEBase(mime['type'], mime['subtype'])
        file = open(attach_file['path'])
        attachment.set_payload(file.read())
        file.close()
        Encoders.encode_base64(attachment)
        msg.attach(attachment)
        attachment.add_header("Content-Disposition",
                              "attachment", filename=attach_file['name'])

    return msg


def send_message(from_addr, to_addrs, msg):
    """
    メールを送信する
    @:param from_addr 差出人
    @:param to_addr 宛先(list)
    @:param msg メッセージ
    """
    smtpobj = smtplib.SMTP(SMTP, PORT)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(GMAIL_ADDR, GMAIL_PW)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


if __name__ == '__main__':

    # 宛先アドレス
    to_addr = "son.munehiro@gmail.com"

    # 件名と本文
    subject = "件名"
    body = "本文"

    # 添付ファイル設定(text.txtファイルを添付)
    mime = {'type': 'text', 'subtype': 'comma-separated-values'}
    attach_file = {'name': 'test.txt', 'path': './text.txt'}

    # メッセージの作成(添付ファイルあり)
    #msg = create_message(GMAIL_ADDR, to_addr, subject, body, mime, attach_file)

    # メッセージ作成(添付ファイルなし)
    msg = create_message(GMAIL_ADDR, to_addr, subject, body)

    # 送信
    send_message(GMAIL_ADDR, [to_addr], msg)
