import time 
import sqlite3 

import bcrypt
from PIL import Image
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

##### Models #####
class ConnectDataBase:
    """
    データベース基底クラス
    """
    def __init__(self, db_path):
        self._db_path = db_path
        self._conn = sqlite3.connect(self._db_path)
        self._cursor = self._conn.cursor()
        self.df = None

    def get_table(self, key="*"):
        self.df = pd.read_sql(f'SELECT {key} FROM userstable', self._conn)
        return self.df

    def close(self):
        self._cursor.close()
        self._conn.close()

    def __del__(self):
        self.close()

class UserDataBase(ConnectDataBase):
    def __init__(self, db_path):
        super().__init__(db_path)
        # dbのカラムの名
        self.__name = "name"
        self.__username = "username"
        self.__password =  "password"
        self.__admin = "admin"
        
        self.__create_user_table()
        self.get_table()

    @property
    def name(self):
        return self.__name  
    @property
    def username(self):
        return self.__username  
    @property
    def password(self):
        return self.__password  
    @property
    def admin(self):
        return self.__admin  

        
    def __create_user_table(self):
        """
        該当テーブルが無ければ作る
        """
        self._cursor.execute('CREATE TABLE IF NOT EXISTS userstable({} TEXT, {} TEXT unique, {} TEXT, {} INT)'.format(self.name, self.username, self.password, self.admin))

    def _hashing_password(self, plain_password):
        """
        平文をハッシュ化する
        """
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def __chk_username_existence(self, username):
        """
        ユニークユーザのバリデーション
        """
        self._cursor.execute('select {} from userstable'.format(self.username))
        exists_users = [_[0] for _ in self._cursor]
        if username in exists_users:
            return True
        
    def add_user(self, name, username, password, admin):
        """
        新しくユーザを追加します
            [args]
                [0] name: str
                [1] username : str (unique only)
                [2] password : str
                [3] admin : bool
            [return]
                res: text (sucsses or field)
        """
        # inputが空かのバリデーション
        if name=="" or username=="" or password=="":
            return
        # ユニークユーザのバリデーション
        if self.__chk_username_existence(username):
            return 
        # 登録
        hashed_password = self._hashing_password(password)
        self._cursor.execute('INSERT INTO userstable({}, {}, {}, {}) VALUES (?, ?, ?, ?)'.format(self.name, self.username, self.password, self.admin),
                                (name, username, hashed_password, int(admin)))
        self._conn.commit()
        return f"{name}さんのアカウントを作成しました"


##### Views #####
class GeneralUserView:
    def main_form(self):
        """
        アクセスの際、最初に表示する内容
        """
        st.header("試作WEBアプリへようこそ！")
        logo = Image.open('./img/login/title_logo2.png')
        st.image(logo, use_column_width=True)

    def side_form(self, model):
        """
        認証フォームの表示と認証オブジェクトの表示
        """
        self.authenticator = stauth.Authenticate(
            model.df[model.name],
            model.df[model.username],
            model.df[model.password],
            'some_cookie_name', 
            'some_signature_key', 
            cookie_expiry_days=0)
        self.authenticator.login("ログイン", "sidebar")


class AdminUserView:
    def __init__(self):
        self.admin_login_flag = None

    def main_form(self, model):
        with st.form(key="create_acount"):
            st.subheader("新規ユーザの作成")
            self.name = st.text_input("ニックネームを入力してください", key="create_user")
            self.username = st.text_input("ユーザー名(ID)を入力してください", key="create_user")
            self.password = st.text_input("パスワードを入力してください",type='password', key="create_pass")
            self.adminauth = st.checkbox("管理者権限の付与")
            self.submit = st.form_submit_button(label='アカウントの作成')
        self.emp = st.empty()

        with st.expander("ユーザテーブルを表示"):
            model.get_table()
            st.table(model.df.drop(model.password, axis=1))

    def side_form(self):
        st.sidebar.write("---")
        st.sidebar.info("adminがキーです")
        return  st.sidebar.text_input("管理者アクセスキー" ,type='password')


class ContactView:
    def _main_form(self):
        st.subheader("💡お問い合わせ先")
        st.write("""
                |🏢 | test |  
                |:--:|:--:|
                |電話番号(内線)📞 | 0000-00-0000 |   
                |メール📧 | hoge_test@example.com |  
        """)

##### Controller #####
class LoginController:
    def __init__(self, db_path):
        self._main_menu = ["Login", "Admin", "Contact"]
        self.choice_menu = st.sidebar.selectbox("メニュー", self._main_menu)

        self.model = UserDataBase(db_path)
        self.gu = GeneralUserView()
        self.au = AdminUserView()
        self.cv = ContactView()

    # 各ページのコントロール
    def _general(self):
        """
        アカウント認証が成功している場合のみ認証オブジェクトと認証情報をsession_stateに返す
        """
        self.gu.main_form()
        self.gu.side_form(self.model)
        auth = 'authentication_status'

        # アカウント認証に成功したとき, ログアウト用のオブジェクトと認証情報を返す
        if st.session_state[auth]:
            st.balloons()
            st.success(f"ようこそ {st.session_state['name']} さん")
            with st.spinner('アカウント情報を検証中...'):
                time.sleep(0.5)

        # アカウント認証の情報が間違っているとき
        elif st.session_state[auth] == False:
            st.error("ログイン情報に誤りがあります。再度入力確認してください。")
            st.warning("アカウントをお持ちでない方は管理者に連絡しアカウントを作成してください")
        # アカウント認証の情報が何も入力されていないとき
        elif st.session_state[auth] == None:
            st.warning("アカウント情報を入力してログインしてください。")

    def _admin(self):
        admin_chk = self.au.side_form()
        if admin_chk == "admin":
            self.au.main_form(self.model)
            if self.au.submit:
                res = self.model.add_user(self.au.name, self.au.username, self.au.password, self.au.adminauth)
                if res:
                    self.au.emp.success(res)
                else:
                    self.au.emp.warning("入力値に問題があるため、登録出来ませんでした")
        elif admin_chk == "":
            st.subheader("アクセスキーを入力してください")
        else:
            st.error("管理者キーが違います")

    # ページを切り替えた際に実行する関数を変える
    def page_choice(self):
        """
        ページの遷移
        """
        if self.choice_menu == self._main_menu[0]:
            self._general()
        if self.choice_menu == self._main_menu[1]:
            self._admin()
        if self.choice_menu == self._main_menu[2]:
            self.cv._main_form()
        

##### Main #####
class Login:
    def __init__(self, db_path):
        """
        DataBaseのパスを受け取ります
        """
        self.controller = LoginController(db_path)
        self.controller.page_choice()


### TEST CODE ###
if __name__ == "__main__":
    Login("db/user.db")
    if st.session_state['authentication_status']:
        if st.button("Bye"):
            st.session_state['authentication_status'] = None
            st.experimental_rerun()





