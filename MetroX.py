import pyxel

D_NONE  = 0

KEY = [None,pyxel.KEY_DOWN,pyxel.KEY_UP,pyxel.KEY_RIGHT,pyxel.KEY_LEFT]
D =   [[0,0],  [0.5,1],[-0.5,-1],[0,0],[0,0]]
DSPEED = [0,  0, 0, 0.1, -0.1]
GPAD = [None,
        pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
        pyxel.GAMEPAD1_BUTTON_DPAD_UP,
        pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
        pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
LAXIS = [None,
         pyxel.GAMEPAD1_AXIS_LEFTY,pyxel.GAMEPAD1_AXIS_LEFTY,
         pyxel.GAMEPAD1_AXIS_LEFTX,pyxel.GAMEPAD1_AXIS_LEFTX]
LAXIS_RANGE = [None,[20000,36000],[-36000,-20000],[20000,36000],[-36000,-20000]]

START_STAGE=0

frame_x = 0
stage_w = 2048
FRAME_W = 120
FRAME_H = 120
FRAME_LIMIT = 88

wspeed = 1
oldspeed = wspeed

tarus    = [ [], [], [], [], [] ]
fumidais = [ [], [], [], [], [] ]
hurdles  = [ [], [], [], [], [] ]

class MyChar():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.is_run = False
        self.jump_cnt = 0
        self.longjump_cnt = 0
        self.muteki_cnt = 0
        self.tumble_cnt = 0
        self.tumble_pose = 0
        self.slow_cnt = 0
        self.is_stageclear = False
    def update(self):
        if self.tumble_cnt > 0:
            pass
        elif self.is_run:
            self.x += wspeed
    def draw(self):
        # ステージクリアした後
        if self.is_stageclear:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16,16, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y, 0, 0,80, 16,16, 7)
        # ジャンプ中
        elif self.jump_cnt > 12:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16+(2-(self.jump_cnt-12)//4)*16,48, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y-24+self.jump_cnt, 0, 0,48, 16,16, 7)
        elif self.jump_cnt > 0:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16+self.jump_cnt//4*16,48, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y-self.jump_cnt, 0, 0,48, 16,16, 7)
        # ロングジャンプ中
        elif self.longjump_cnt > 24:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16+(2-(self.longjump_cnt-24)//8)*16,48, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y-96+self.longjump_cnt*2, 0, pyxel.frame_count//4%4*16,64, 16,16, 7)
        elif self.longjump_cnt > 0:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16+self.longjump_cnt//8*16,48, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y-self.longjump_cnt*2, 0, pyxel.frame_count//4%4*16,64, 16,16, 7)
        # 転倒中
        elif self.tumble_cnt > 0:
            if pyxel.frame_count//4%2==0:
                pyxel.blt(self.x-frame_x,self.y+3, 0, 16,16, 16,16, 7)
                pyxel.blt(self.x-frame_x,self.y,   0,  self.tumble_pose*16,64, 16,16, 7)
        # 走り中
        elif self.is_run:
            if self.muteki_cnt==0 or pyxel.frame_count%2==0:
                pyxel.blt(self.x-frame_x,self.y+3, 0, 16,16, 16,16, 7)
                pyxel.blt(self.x-frame_x,self.y, 0, pyxel.frame_count//4%4*16,32, 16,16, 7)
        # 開始待ち中
        else:
            pyxel.blt(self.x-frame_x,self.y+3, 0, 16,16, 16,16, 7)
            pyxel.blt(self.x-frame_x,self.y, 0, 0,16, 16,16, 7)
myChar = MyChar(12,59)

class Taru():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.is_alive= True
    def update(self):
        self.x -= 0.5
        if self.x - frame_x < -16:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x-frame_x,self.y, 0, 80+(4000-self.x)//2%8*10,16, 10,12, 7)

class Fumidai():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.is_alive = True
        self.fumi_cnt = 0
    def update(self):
        if self.x - frame_x < -16:
            self.is_alive = False
        if self.fumi_cnt > 0:
            self.fumi_cnt -= 1
    def draw(self):
        if self.fumi_cnt == 0:
            pyxel.blt(self.x - frame_x, self.y, 0, 192,16, 16,16, 15)
        else:
            pyxel.blt(self.x - frame_x, self.y, 0, 208,16, 16,16, 15)

class Hurdle():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.is_alive = True
        self.is_stand = True
    def update(self):
        if self.x - frame_x < -16:
            self.is_alive = False
    def draw(self):
        if self.is_stand:
            pyxel.blt(self.x - frame_x, self.y, 0, 224,16, 16,16, 15)
        else:
            pyxel.blt(self.x - frame_x, self.y, 0, 240,16, 16,16, 15)


class App():
    def __init__(self):
        pyxel.init(120,120,title="MetroX",fps=48)
        pyxel.load("runner.pyxres")
        self.init_game()
        pyxel.run(self.update,self.draw)

    def init_game(self):
        self.stage_num = 0
        self.init_stage()

    def init_stage(self):
        global frame_x,tarus,fumidais,hurdles
        self.stage_num += 1
        self.cnt = 0
        frame_x = 0
        myChar.x = 12
        myChar.y = 59
        myChar.is_run = False
        myChar.jump_cnt = 0
        myChar.longjump_cnt = 0
        self.stageclear_cnt = 0
        self.gamestart_cnt = 144
        tarus    = [[],[],[],[],[]]
        fumidais = [[],[],[],[],[]]
        hurdles  = [[],[],[],[],[]]
        self.checkedtile_x = 0
        myChar.is_stageclear = False

    def update(self):
        global frame_x,stage_w,wspeed,oldspeed,tarus,fumidais,hurdles
        ### ゲーム状態の遷移に伴う処理
        # ステージクリアした後
        if self.stageclear_cnt > 0:
            self.stageclear_cnt -= 1
            if self.stageclear_cnt==0:
                self.init_stage()
            return
        # ゲーム開始カウントダウン
        if self.gamestart_cnt > 0:
            self.gamestart_cnt -= 1
            if self.gamestart_cnt == 0:
                myChar.is_run = True
            return
        # ステージクリアの判定
        if myChar.x > stage_w - 40:
            myChar.is_stageclear = True
            self.stageclear_cnt = 140
        ### ステージごとのカウンター
        self.cnt += 1
        ### オブジェクト（踏み台、ハードル、）の生成
        self.frx = frx = int(frame_x)
        tile_x = (frx+120)//8
        if tile_x != self.checkedtile_x:
            self.checkedtile_x = tile_x
            # 踏み台（ジャンプ台）
            tile_num = pyxel.tilemaps[0].pget((frx+120)//8,(self.stage_num-1)*32+14)
            if tile_num[1]==2:
                for i in range(5):
                    if (int(tile_num[0]) & int(2**i))!=0:
                        fumidais[i].append(Fumidai(frx+120+4*i,56+8*i))
            # 樽
            tile_num = pyxel.tilemaps[0].pget((frx+120)//8,(self.stage_num-1)*32+15)
            if tile_num[1]==3:
                for i in range(5):
                    if (int(tile_num[0]) & int(2**i))!=0:
                        tarus[i].append(Taru(frx+120+4*i,56+8*i+3))
            # ハードル
            tile_num = pyxel.tilemaps[0].pget((frx+120)//8,(self.stage_num-1)*32+16)
            if tile_num[1]==4:
                for i in range(5):
                    if (int(tile_num[0]) & int(2**i))!=0:
                        hurdles[i].append(Hurdle(frx+120+4*i,56+8*i))
        ### 床に沿って移動速度を変更
        if myChar.jump_cnt==0 and myChar.longjump_cnt==0:
            tile = pyxel.tilemaps[0].pget((myChar.x+12)//8,(self.stage_num-1)*32+(myChar.y+16)//8)
            if 21<=tile[1]<=22:
                myChar.slow_cnt = 48
                oldspeed = wspeed
                wspeed = 0.6
        if myChar.slow_cnt > 0:
            myChar.slow_cnt -= 1
            if myChar.slow_cnt == 0:
                wspeed = oldspeed
        ### マイキャラのイベント処理
        # 無敵状態（かな？）のカウントダウン
        if myChar.muteki_cnt > 0:
            myChar.muteki_cnt -= 1
        # ジャンプ中
        if myChar.jump_cnt > 0:
            myChar.jump_cnt -= 1
        # ロングジャンプ中
        if myChar.longjump_cnt > 0:
            myChar.longjump_cnt -= 1
            if myChar.longjump_cnt == 0:
                wspeed = oldspeed
        # 転んでる最中はプレイヤーが何もできない
        if myChar.tumble_cnt > 0:
            myChar.tumble_cnt -= 1
            if myChar.tumble_cnt == 0:
                wspeed = oldspeed
            #myChar.x += 1
        # ジャンプ開始？
        elif (myChar.jump_cnt==0 and myChar.longjump_cnt==0) and (pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_SPACE)):
            oldspeed = wspeed
            lane = (myChar.y-46)//8 #どのレーンを走ってるか？
            for fumi in fumidais[lane]:
                if myChar.x+8>fumi.x and fumi.x+10>myChar.x:
                    fumi.fumi_cnt = 8
                    myChar.slow_cnt = 0
                    wspeed = 3
                    myChar.longjump_cnt = 48
            if myChar.longjump_cnt==0:
                myChar.jump_cnt = 24
        # 移動用キー入力の判定
        else:
            self.lst = []
            for i in range(1,5):
                if pyxel.btn(KEY[i]) or (LAXIS_RANGE[i][0] < pyxel.btnv(LAXIS[i]) < LAXIS_RANGE[i][1]) or pyxel.btn(GPAD[i]):
                    wspeed += DSPEED[i]
                    myChar.y += D[i][1]
                    myChar.y = max(min(83,myChar.y), 51)
                    if 51 < myChar.y < 83:
                        myChar.x += D[i][0]

        #myChar.x = min(frame_x + 50,myChar.x)
        ### マイキャラの状態ごとの移動可能スピード量調整
        if myChar.slow_cnt > 0:
            wspeed = 0.6
        elif myChar.longjump_cnt > 0:
            wspeed = max(min(3, wspeed), 1)
        elif myChar.jump_cnt > 0:
            wspeed = max(min(1.6, wspeed), 1)
        else:
            wspeed = max(min(2, wspeed), 1)

            

        ### マイキャラの更新
        myChar.update()

        # キャラ移動に沿った背景スクロール処理
        if myChar.x-frame_x > FRAME_W - FRAME_LIMIT and frame_x != stage_w - FRAME_W:
            frame_x += wspeed
            if frame_x > stage_w - FRAME_W:
                frame_x = stage_w - FRAME_W
        # ステージ両端における移動可能範囲の処理
        myChar.x = max(min(stage_w - 16,myChar.x), 0)

        ### ハードルの更新
        for hrec in hurdles:
            for hurdle in reversed(hrec):
                hurdle.update()
                if not hurdle.is_alive:
                    hrec.remove(hurdle)
        ### 樽の更新
        for tarurec in tarus:
            for taru in reversed(tarurec):
                taru.update()
                if not taru.is_alive:
                    tarurec.remove(taru)
        ### 踏み台の更新
        for fumirec in fumidais:
            for fumi in reversed(fumirec):
                fumi.update()
                if not fumi.is_alive:
                    fumirec.remove(fumi)
        
        ### 当たり判定
        # 樽
        if myChar.jump_cnt == 0 and myChar.longjump_cnt==0:
            lane = (myChar.y-46)//8 #どのレーンを走ってるか？
            # 樽
            for taru in tarus[lane]:
                if abs((taru.x-5)-(myChar.x-8)) < 10:
                    oldspeed = wspeed
                    myChar.tumble_cnt = 36
                    myChar.tumble_pose = 3
            # ハードル
            for hdl in hurdles[lane]:
                if abs((hdl.x)-(myChar.x-8)) < 6 and hdl.is_stand:
                    hdl.is_stand = False
                    oldspeed = wspeed
                    myChar.tumble_cnt = 36
                    myChar.tumble_pose = 5


    def draw(self):
        ### 背景描画
        pyxel.cls(0)
        pyxel.bltm(0,0, 0, frame_x,(self.stage_num-1)*256, FRAME_W,FRAME_H)
        ### デバッグ用
        pyxel.bltm(0,112, 0, frame_x,(self.stage_num-1)*256+128, FRAME_W,8)

        ### 踏み台の描画
        for i in range(5):
            for fumi in fumidais[i]:
                fumi.draw()
        ### 樽の描画
        for i in range(5):
            for taru in tarus[i]:
                taru.draw()
        ### ハードルの描画
        for i in range(5):
            for hurdle in hurdles[i]:
                hurdle.draw()
        ### マイキャラの描画
        myChar.draw()

        if self.gamestart_cnt > 0:
            pyxel.text(50,20, "READY\n\n  {}".format(self.gamestart_cnt//48+1),8)

        ###### デバッグ用 ###########################
        #pyxel.text(10,10, "frame_x:{}".format(frame_x),7)
        pyxel.text(10,10, "wspeed:{}".format(wspeed),7)
        pyxel.text(10,20, "stagecelar_cnt:{}".format(self.stageclear_cnt),7)
        #pyxel.text(10,10, "TILE: {}".format(pyxel.tilemaps[0].pget((myChar.x+12)//8,(self.stage_num-1)*32+(myChar.y+16)//8)),7)
        #pyxel.text(10,20, "x:  {}".format((myChar.x+12)//8),7)
        #pyxel.text(10,30, "y:  {}".format((myChar.y+16)//8),7)
        #pyxel.text(10,20, "myChar.x:{}".format(myChar.x),7)
        #pyxel.text(70,20, "myChar.x-frame_x:\n{}".format(myChar.x-frame_x),7)
        pyxel.text(10,30, "myChar.y:{}".format(myChar.y),7)
        #pyxel.text(10,30, "myChar.tumble_cnt:{}".format(myChar.tumble_cnt),7)
        #pyxel.text(10,40, "Lane:{}".format((myChar.y-46)//8),7)
        #pyxel.text(10,50, "myChar.jump_cnt:{}".format(myChar.jump_cnt),7)

App()

