#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import math
from enum import IntEnum
import pandas as pd


def random_name(name_length=4):
    name = ""
    for i in range(0, name_length):
        name += random_hira()
    return name


def random_hira():
    hira = uwords("ぁ", "ん")
    hira_len = len(hira)
    return list(hira)[random.randint(0, hira_len-1)]


def uwords(fword, lword):
    """ From: https: // qiita.com/22C8/items/4dd50945b73e22c6aded """
    """ ユニコード連続文字 """
    return {chr(n) for n in range(ord(str(fword)),  ord(str(lword)), +1)}


class Brave:
    """ 勇者を表現するクラス """

    def __init__(self, personality):
        self.name = random_name()
        self.lv = 1
        # 性格
        self.personality = personality
        self.str = 10
        self.agi = 8
        self.vit = 8
        self.int = 4
        self.luk = 5

    def lvup(self):
        lvup_util = LvupUtil()
        self.lv += 1
        incr_params = lvup_util.get_incr_params(self)
        self.str += incr_params['str']
        self.agi += incr_params['agi']
        self.vit += incr_params['vit']
        self.int += incr_params['int']
        self.luk += incr_params['luk']

        print(f"Lv: {self.lv}, 性格: {self.personality}")
        print(f"{self.name}は レベルが あがった")
        print(f"ちからが {incr_params['str']}ポイント あがった！")
        print(f"すばやさが {incr_params['agi']}ポイント あがった！")
        print(f"たいりょくが {incr_params['vit']}ポイント あがった！")
        print(f"かしこさが {incr_params['int']}ポイント あがった！")
        print(f"うんのよさが {incr_params['luk']}ポイント あがった！")
        print("")

    def __str__(self):
        return f"{self.name},{self.lv},{self.personality},{self.str},{self.agi},{self.vit},{self.int},{self.luk}\n"


class LvupUtil:
    """ レベルアップ時の数値データ用ユーティリティクラス """

    # ファイル読み込みするのでシングルトンに
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 基礎上昇値、最大値、最小値のデータを読み込み(Lvを行名に採用)
            cls._instance.base_incr = pd.read_csv('base_incr.csv', index_col=0)
            # 性格名と性格補正値のデータを読み込み(性格名を行名に採用)
            cls._instance.psn_incr = pd.read_csv('psn_incr.csv', index_col=0)
        return cls._instance

    def personality_list(self):
        # 性格一覧リスト
        return list(self.psn_incr.index.values.flatten())

    def get_incr_params(self, brave):
        lv = brave.lv
        personality = brave.personality
        incr_params = dict(str=0, agi=0, vit=0, int=0, luk=0)
        # TODO: 最大値、最小値処理が必要
        for status_type in set(['str', 'agi', 'vit', 'int', 'luk']):
            base = self.base_incr.at[lv, 'base_' + status_type]
            offset = self.psn_incr.at[personality, 'offset_' + status_type]
            rnd = random.randint(0, 255)
            incr_params[status_type] = math.floor(
                base * (rnd / 128) * (offset / 128))
        return incr_params


if __name__ == '__main__':
    lvup_util = LvupUtil()
    with open('output.csv', 'w') as f:
        for personality in lvup_util.personality_list():
            # 各性格ごとに勇者を100人作り一定のレベルまで上げる
            for n in range(0, 100):
                b = Brave(personality)
                for i in range(0, 39):
                    b.lvup()
                # 出来上がったら出力
                f.write(b.__str__())
