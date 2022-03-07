#旧仕様のデッキ配布(.ydk)の記述は消しました
#旧DiscordBotを参照のこと


########################################################################
#トークンを置く
TOKEN = 'NTg1NDAyMzczNDA5NjAzNTg2.XPY8fg.QC9pmgooshmpVJ5C890ZVMmRiiI'
#
########################################################################


#coding: UTF-8
from time import sleep
import discord
import random
import glob
import os
import asyncio
import datetime

#新デッキ用？
import csv
import pprint

#変数
path = os.getcwd()
bgm_path = path+'/bgm'
dirs = os.listdir(bgm_path)
sound_volume = 0.028
check_var = 0    #bgm再生リスト用変数

list_num= 0    #新式デッキカウンタ

loglist = [449571660773720065,801811993672679436]#general,bot操作用のみログ取り


#新デッキ方式の変数


commandlist =["/bgm","/stop","/next","/volu","/vold","/del","/reset","/help","/duel","/duel_s","/change","/bgmlist","/show_bgm","/plz_bgm","/show_deck","/deck","/deck_add"]

bgmlist=[["通常BGM",'/bgm'],["遊戯王",'/bgm/yugioh']]

#ランダムデュエル用乱数生成
with open('deck.csv',mode='r+') as f:
    reader = csv.reader(f)
    l = [row for row in reader]
mylist = random.sample(list(range(1, len(l)+1)), len(l))#デッキ数を確認





#全角半角文字数左揃え
import unicodedata
def left(digit, msg):
    count = 0
    for c in msg:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return msg+" "*(digit - count)
def right(digit, msg):
    count = 0
    for c in msg:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return " "*(digit - count)+msg




#接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event

async def on_ready():

    # 起動したらターミナルにログイン通知
    print('起動完了')
    print(mylist)



@client.event
async def on_voice_state_update(member,before,after):#ボイチャ検知

    guild = discord.utils.get(client.guilds, name="ゲーム枠")
    channel = discord.utils.get(guild.text_channels, name="ログ")

    now = datetime.datetime.now()
    if before.channel==None:

        await channel.send(str(now)+"\n"+member.name+'VC接続')#ログのチャンネルに書き込む

        print(now)
        print(member.name+'VC接続')
        print("\n")
        with open('general.txt', 'a') as f: #発言ぶっこ抜き
            print(now,file = f)
            print(member.name+'VC接続',file = f)
            print("\n",file= f)
    elif after.channel==None:

        await channel.send(str(now)+"\n"+member.name+'VC解除')#ログのチャンネルに書き込む
        

        print(now)
        print(member.name+'VC解除')
        print("\n")
        with open('general.txt', 'a') as f: #発言ぶっこ抜き
            print(now,file = f)
            print(member.name+'VC解除',file = f)
            print("\n",file= f)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):#メッセージ検知

    guild = discord.utils.get(client.guilds, name="ゲーム枠")
    channel = discord.utils.get(guild.text_channels, name="ログ")

    if message.author.bot:
        return
    else:
        now = datetime.datetime.now()
        with open('general.txt', 'a') as f: #発言ぶっこ抜き
            #print("["+message.channel.name+"]",file = f)
            #print(now,file = f)
            #print(message.author,file= f)
            #print(message.content,file = f)

            print("["+message.channel.name+"]"+" ["+str(now)+"] "+str(message.author)+"\n"+str(message.content) ,file = f)

            print("\n",file= f)

        print("["+message.channel.name+"]")
        print(now)
        print(message.author)
        print(message.content)
        print("\n")

        if message.channel.id != 921304969523642398:#ログチャンネルは除外
            m =  "["+message.channel.name+"]"+" ["+str(message.author)+"] "+str(now)+"\n"+str(message.content)+"\n "
            await channel.send(m.replace('@', '@ '))#ログのチャンネルに書き込む&メンション防止



#メッセージ受信時に処理する関数
    global voice,sound_volume,list_num,mylist,check_var,path,dirs,bgm_path

    vs = random.randint(1,3)


#新方式対応デッキ(パスワード制)
    if '/deck_add ' in message.content :
        hoge = message.content.split()#[/deck_add,デッキ名,パスワード]の配列
        now = datetime.date.today()#日時
        result = False
        #上書きの場合
        with open('deck.csv',mode='r+') as f:
            reader = csv.reader(f)
            l = [row for row in reader] #deck.csvの二次元配列
        for i in l:
            if hoge[1] in i:#デッキ名ヒット
                t = l.index(i) #iは何行目？
                for j in l[t]:
                    if str(message.author) in j:#作者も合致
                        result = True
                        break
                if result == True:
                    break

        if result == True:
            t = l.index(i) #iは何行目？
            del l[t] #消す
            l.insert(t,[hoge[1],message.author,now, hoge[2]])
            with open('deck.csv', 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(l)
            await message.channel.send(hoge[1]+"デッキを上書きしたよ。よかったよね？")

        else:#新規
            l.append([hoge[1],message.author,now, hoge[2]])#末尾に追加
            with open('deck.csv', 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(l)
            await message.channel.send(hoge[1]+"デッキを追加したよ.")



#デッキを消す
    if '/deck_del ' in message.content :
        hoge = message.content.split()#[/deck_add,番号]の配列
        num = int(hoge[1])
        with open('deck.csv',mode='r+') as f:
            reader = csv.reader(f)
            l = [row for row in reader] #deck.csvの二次元配列
            name = l[[num-1][0]]
            del l[num-1] #消す
            with open('deck.csv', 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(l)
            await message.channel.send(str(name[0])+"デッキを削除したよ。よかったよね？")

#デッキ一覧を返す
    if  message.content == '/show_deck' :
        i = 0
        with open('deck.csv') as f:
            reader = csv.reader(f)
            n = ""
            for row in reader:
                i+=1
                row2 = left(3,str(i)) +":"+left(50,str(row[0]))+left(30,str(row[1]))+right(14,str(row[2]))
                n = n+"\n"+ row2
                if i % 10 == 0: #多すぎるとバグるので10行で一回出力
                    await message.channel.send("`"+n+"`")
                    n= ""
            if n=="":#偶然10行ジャストでnが空
                pass
            else:
                await message.channel.send("`"+n+"`")

#指定したデッキ番号のデッキを渡す
    if '/deck_num ' in message.content :
        hage = message.content.split()#[/deck_num , デッキ番号]の配列
        with open('deck.csv') as f:
            reader = csv.reader(f)
            l = [row for row in reader]
            a = int(hage[1])#要求番号

        await message.channel.send(l[a-1][0])#デッキ名
        await message.channel.send(l[a-1][3])#パスワード

#新ランダム
    if message.content =='/duel':

        with open('deck.csv') as f:
            reader = csv.reader(f)
            l = [row for row in reader]
        await message.channel.send("プレイヤー順は勝手に決めてください")
        await message.channel.send("[プレイヤー1]\n> "+l[mylist[list_num]-1][3])#パスワード
        await message.channel.send("[プレイヤー2]\n> "+l[mylist[list_num+1]-1][3])#パスワード
        await message.channel.send("[プレイヤー3]\n> "+l[mylist[list_num+2]-1][3])#パスワード
        await message.channel.send("[プレイヤー4]\n> "+l[mylist[list_num+3]-1][3])#パスワード

       

        print("使用デッキ："+l[mylist[list_num]-1][0]+","+l[mylist[list_num+1]-1][0]+","+l[mylist[list_num+2]-1][0]+","+l[mylist[list_num+3]-1][0])
        list_num += 4
        vs = random.randint(1,3)
        if vs == 1:
            await message.channel.send('**対戦組み合わせ:[1][2]vs[3][4]**')
        elif vs == 2:
            await message.channel.send('**対戦組み合わせ:[1][3]vs[2][4]**')
        else:
            await message.channel.send('**対戦組み合わせ:[1][4]vs[2][3]**')

#新ランダム(1vs1)
    if message.content =='/duel_s':

        with open('deck.csv') as f:
            reader = csv.reader(f)
            l = [row for row in reader]
        await message.channel.send("[プレイヤー1]\n> "+l[mylist[list_num]-1][3])#パスワード
        await message.channel.send("[プレイヤー2]\n> "+l[mylist[list_num+1]-1][3])#パスワード



        print("使用デッキ："+l[mylist[list_num]-1][0]+","+l[mylist[list_num+1]-1][0])
        list_num += 2
        vs = random.randint(1,3)



        
#BGMプレーヤー


    #再生
    if  message.content == '/bgm' :
        voice = await message.author.voice.channel.connect()
        bgm_play()

        while True:
            if voice.is_playing()==False:
                voice.stop()
                bgm_play()
            else:
                await asyncio.sleep(1)

    #再生リスト変更
    if message.content =='/change' and check_var >= len(bgmlist)-1:
        check_var = 0
        await message.channel.send("曲リスト:" + bgmlist[check_var][0])
        dirs = os.listdir(path+bgmlist[check_var][1])

    elif message.content =='/change' and check_var < len(bgmlist)-1:
        check_var += 1
        await message.channel.send("曲リスト:" + bgmlist[check_var][0])
        dirs = os.listdir(path+bgmlist[check_var][1])





    #再生停止(切断)
    if message.content =='/stop':
        check_var = 0
        await voice.disconnect()

    #チェンジ
    if message.content =='/next':
        voice.stop()
        bgm_play()

        while True: #ループ部
            if voice.is_playing()==False:
                voice.stop()
                bgm_play()
            else:
                await asyncio.sleep(1)

    #音量アップ
    if message.content =='/volu':
        sound_volume= 1.5
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = sound_volume
        sound_volume= 0.04

    #音量ダウン
    if message.content =='/vold':
        sound_volume = 0.66
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = sound_volume
        sound_volume= 0.04

    #BGMリスト表示
    if message.content =='/bgmlist':
        await message.channel.send(dirs)

    #BGM参照
    if message.content =='/show_bgm':
        await message.channel.send(playing_music[:playing_music.find('.')])

    #BGMくだしあ
    if message.content =='/plz_bgm':
        try:
            await message.channel.send(playing_music[:playing_music.find('.')])
            await message.channel.send(file=discord.File(music))
        except:
            await message.channel.send("たぶん元ファイルが8MB以上です、ごめんね")

   #一括削除
    if message.content =='/del':
        await message.channel.purge(check=is_me)
        await message.channel.send('削除完了')

    #デッキをシャッフル
    if message.content =='/reset':
        with open('deck.csv',mode='r+') as f:
            reader = csv.reader(f)
            l = [row for row in reader]
        mylist = random.sample(list(range(1, len(l)+1)), len(l))#デッキ数を確認
        list_num = 0
        await message.channel.send('デッキリセット実行完了')



     #コマンド一覧
    if message.content =='/help':
        m ="`[Duel bot 操作コマンド　/+単語で発動]"+"\n"+"\n"\
          +"duel".ljust(30," ")+"ランダムタッグ配布(パスワード制)"+"\n"\
          +"duel_s".ljust(30," ")+"ランダム1on1(パスワード制)"+"\n"\
          +"show_deck".ljust(30," ")+"格納済みデッキ一覧を返す"+"\n"\
          +"deck_add デッキ名 内容(ydke:~)".ljust(30," ")+"デッキ追加(同作者同名デッキは上書き)"+"\n"\
          +"deck_del デッキ番号".ljust(30," ")+"指定の番号のデッキを消す"+"\n"\
          +"deck_num デッキ番号".ljust(30," ")+"指定番号のデッキを表示"+"\n"\
          +"reset".ljust(30," ")+"duelコマンドにおけるデッキ選定のリセット"+"\n"\
          +"bgm".ljust(30," ")+"bgmを流す"+"\n"\
          +"-----------------BGM再生中に使用可能-------------------"+"\n"\
          +"next".ljust(30," ")+"bgmを変える"+"\n"\
          +"change".ljust(30," ")+"bgmの再生リストを変える"+"\n"\
          +"volu".ljust(30," ")+"ボリュームアップ"+"\n"\
          +"vold".ljust(30," ")+"ボリュームダウン"+"\n"\
          +"stop".ljust(30," ")+"botをボイスチャンネルから切断する"+"\n"\
          +"show_bgm".ljust(30," ")+"bgmのタイトルを教えてくれる"+"\n"\
          +"plz_bgm".ljust(30," ")+"bgmの音声ファイルをくれる※テスト中"+"\n"\
          +"----------------------------------------------------------------------"+"\n"\
          +"del".ljust(30," ")+"Botによる発言とBotに対するコマンド宣言の削除`"+"\n"

        await message.channel.send(m)
    




#削除内容
def is_me(m):
    return (m.channel.id != 921304969523642398) and (m.author == client.user or m.content in commandlist)
    #ログチャンネル以外かつbotとbot命令を削除

#再生def
def bgm_play():
    global music ,playing_music
    playing_music =random.choice(dirs)
    music =  path+bgmlist[check_var][1]+"/"+playing_music
    voice.play(discord.FFmpegPCMAudio(music,executable='ffmpeg'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = sound_volume




# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
