## こちらの記事を丸々コピー
## https://www.okb-shelf.work/entry/what_bloom_filter

'''
ブルームフィルター
Wiki:https://ja.wikipedia.org/wiki/%E3%83%96%E3%83%AB%E3%83%BC%E3%83%A0%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF

Burton H. Bloomによって発明された確率的データ構造

あるデータが集合の要素かどうかの判定に使われる
含まれているのに含まれていると判定することもある
集合に要素を追加していくにつれて偽陽性の可能性が増す

今回丸コピするサイトの内容を拝借すると
確率的データ構造とは「「値がデータ構造に入っているか、いないかをを知ることが出来るデータ構造」

'''

import functools

class BloomFilter:
    def __init__(self, filter_size):
        # サイズfilter_sizeのブルームフィルタを作成
        self.filter_size = filter_size
        self.bloom_filter = [0 for _ in range(filter_size)]
    
    # 
    def set_v(self, val):
        indexes = self.n_hash(val)
        for index in indexes:
            self.bloom_filter[index] = 1
    
    def exist_v(self, val):
        indexes = self.n_hash(val)
        for index in indexes:
            if self.bloom_filter[index] == 0:
                return False
        return True
    
    def n_hash(self, val):
        #　valをハッシュ化して、文字列に変換して、各文字をintに変換して、リストに格納
        hashed = abs(hash(val))
        # hashedのデバッグ用  ex-) bf.set_v("sample")->7680050255917352597
        # print(hashed)
        d_list = [int(n) for n in str(hashed)]
        return [
            # 
            self._hash_common(lambda a, b: a + b, d_list),
            self._hash_common(lambda a, b: a + 2 * b, d_list),
        ]
        
    def _hash_common(self, func, d_lst):
        # functools.reduceは、第一引数の関数を第二引数のリストに対して実行する。
        # 第三引数は初期値が0であることを示す
        execed = abs(functools.reduce(func, d_lst, 0))
        while execed >= self.filter_size:
            execed = execed / self.filter_size
        return int(execed)
    
# bf = BloomFilter(10)
# bf.set_v(3)
# print(bf.exist_v(3)) # True
# print(bf.exist_v(10)) # False
# print(bf.exist_v(11)) # False
# print(bf.exist_v(30)) # True

# ↑近い値はTrueになる

bf = BloomFilter(30)
# 入れる番号が増えると偽陽性が減った
# selected_number = [1,3,4,7,9,12,16,20,24]
selected_number = [1,3,4,7,9,12,16,20,24,88, 89, 91, 92, 93, 94, 95, 96, 97, 98]
for n in selected_number:
  bf.set_v(n)
print(bf.bloom_filter)

for n in selected_number:
    result = bf.exist_v(n)
    print("{n}:{result}".format(n=n, result=result))

not_exist_numbers = list(set([n for n in range(1, 101)]) - set(selected_number))
giyousei_set = set()
for n in not_exist_numbers:
    result = bf.exist_v(n)
    if(result == True):
        print("{n}:{result}".format(n=n, result=result))
        giyousei_set.add(n)

diff = set(not_exist_numbers) - giyousei_set

print(diff)
        