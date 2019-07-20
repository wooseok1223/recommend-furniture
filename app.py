# -- coding: utf-8 --
from flask import Flask, render_template, request , redirect ,url_for
import pymysql
import pandas as pd
import numpy as np
from tqdm import tqdm

app = Flask(__name__)

### class 스크립트


class cbf_recommender():
    def __init__(self, df_merged, rating):
        self.df_merged = None
        self.rating = None

        self.df_item = None
        self.df_user = None
        self.df_predict = None
        self.user_no = None

        # 여기서, df_item은 사용자에게 보여진 이미지들의 feature vectors

    def get_user_profile(self, df_item, rating):
        self.df_item = df_item

        # feature 자체에 값이 없는 경우 제거 (or 웹용 데이터 선정시 부터 제거)
        df_item_wd = df_item[df_item.sum(axis=1) > 0]
        rating_wd = rating[df_item.sum(axis=1) > 0]

        # Q) feature 값의 normalization 해야할까?
        # ex) 가구 2개 시, 가구 하나에 약 0.7
        df_item_normalized = df_item_wd.apply(lambda x: x / np.sqrt(df_item_wd.sum(axis=1)))

        # get all the user number
        user_no = rating.columns
        self.user_no = user_no  # ?

        # create an empty dataframe
        df_user = pd.DataFrame(columns=df_item.columns)

        for i in tqdm(range(len(user_no))):
            working_df = df_item_normalized.mul(rating_wd.iloc[:, i], axis=0)
            # working_df.replace(0, np.NaN, inplace=True)
            df_user.loc[user_no[i]] = working_df.mean(axis=0)

        return df_user

    # 여기서 df_item 은 추천에 사용될 이미지들 (웹에서 보여지지 않은 이미지들)
    def predict(self, df_user, df_item):
        self.df_user = df_user  # ?
        # get all the user number
        user_no = df_user.index

        # normalization
        df_item_normalized = df_item.apply(lambda x: x / np.sqrt(df_item.sum(axis=1)))

        # make an empty dataframe
        df_predict = pd.DataFrame()

        # user predict by tfidf
        for i in tqdm(range(len(user_no))):
            working_df = df_item_normalized.mul(df_user.iloc[i], axis=1)
            df_predict[user_no[i]] = working_df.sum(axis=1)

        # predict 가 0 일 경우 Nan으로 변환 ?
        # feature 값 0 인 것 제외했으니 괜찮으려나
        # 이 후, 추천 목록에 추가하기 위한 방법을 고민해볼 수 있을 듯 (빈도수 등을 활용해 다른 feature들 활용하는 등)
        # df_predict.replace(0, np.NaN, inplace=True)

        return df_predict

    def recommend(self, df_predict, user_no):

        self.df_predict = df_predict
        # get all item id
        item_id = df_predict.index

        # user predicted rating to all books
        user_predicted_rating = df_predict[[user_no]]

        # items already exposed to user (여기선 보여준 적 없는 이미지들만 사용해서 추천)
        # already_exposed = df_merged[df_merged['user_id'].isin([user_no])]['item_id']

        # recommendation without items being exposed to user
        # all_rec = user_predicted_rating[~user_predicted_rating.index.isin(already_exposed)]
        all_rec = user_predicted_rating

        return all_rec.sort_values(by=user_no, ascending=False).iloc[0:6]


class Db_process:

    def data_process_bedroom(self, src):
        for i in src.split(","):
            self.filesrc.append(i)

        return self.filesrc


    def data_process_dataframe(self):
        df2 = pd.DataFrame(self.filesrc)
        df2 = df2.rename(columns={0: 'img'})
        return df2


class MysqlController:
    def __init__(self, host, id, pw, db_name, pt):
        self.conn = pymysql.connect(host=host, user=id, password=pw, database=db_name, port=pt)
        self.curs = self.conn.cursor()
        self.src = None

    def select_total(self,src):
        sql = "SELECT * FROM final_furniture715 where img LIKE '%{}%' OR img LIKE '%{}%'OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%'".format(src[0],src[1],src[2],src[3],src[4],src[5],src[6],src[7],src[8],src[9])
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data
    def select_total2(self,src):
        sql = "SELECT * FROM final_furniture715 where img LIKE '%{}%' OR img LIKE '%{}%'OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%'".format(src[0],src[1],src[2],src[3],src[4],src[5],src[6],src[7],src[8],src[9])
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data

    def select_total3(self,src):
        if 'livingroom' in src[0]:
            sql = "SELECT * FROM final_furniture715 where img LIKE '%recommend%' and place like '%living%'"
        else:
            sql = "SELECT * FROM final_furniture715 where img LIKE '%recommend%' and place like '%bed%'"
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data

    def select_color1(self,src):
        sql = "SELECT * FROM final_color715 where img LIKE '%{}%' OR img LIKE '%{}%'OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%'".format(src[0],src[1],src[2],src[3],src[4],src[5],src[6],src[7],src[8],src[9])
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data
    def select_color2(self,src):
        sql = "SELECT * FROM final_color715 where img LIKE '%{}%' OR img LIKE '%{}%'OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%'".format(src[0],src[1],src[2],src[3],src[4],src[5],src[6],src[7],src[8],src[9])
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data

    def select_color3(self,src):
        if 'livingroom' in src[0]:
            sql = "SELECT * FROM final_color715 where img LIKE '%recommend%' and place like '%living%'"
        else:
            sql = "SELECT * FROM final_color715 where img LIKE '%recommend%' and place like '%bed%'"
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data

    def select_style1(self,src):
        sql = "SELECT * FROM final_style715 where img LIKE '%{}%' OR img LIKE '%{}%'OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%'".format(src[0],src[1],src[2],src[3],src[4],src[5],src[6],src[7],src[8],src[9])
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data
    def select_style2(self,src):
        sql = "SELECT * FROM final_style715 where img LIKE '%{}%' OR img LIKE '%{}%'OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%' OR img LIKE '%{}%'".format(src[0],src[1],src[2],src[3],src[4],src[5],src[6],src[7],src[8],src[9])
        print(sql)
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data

    def select_style3(self,src):
        if 'livingroom' in src[0]:
            sql = "SELECT * FROM final_style715 where img LIKE '%recommend%' and place like '%living%'"
        else:
            sql = "SELECT * FROM final_style715 where img LIKE '%recommend%' and place like '%bed%'"
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data

    def result_img(self,src):
        sql = "SELECT img FROM final_style715 where id = {} or id = {} or id = {} or id = {} or id = {} or id = {}".format(src[0],src[1],src[2],src[3],src[4],src[5])
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        data = []
        for i in result:
            data.append(i)
        return data



@app.route('/')
def main():
    return render_template('home.html')

@app.route('/first')
@app.route('/first<int:src>')
def first():
    return render_template('FirstPage.html')

@app.route('/result',methods=['POST'])
def result():
    if request.method == 'POST':
        filesrc = []
        temp = request.form['src']
        for i in temp.split(","):
            filesrc.append(i)
            print(i)
        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        result = mysql_controller.select_total(filesrc)
        df1_fur = pd.DataFrame(result)
        df1_fur = df1_fur.rename(columns={0: 'id',1: 'img',2: 'place', 3: 'chair', 4: 'sofa', 5: 'pottedplant', 6:
            'bed', 7: 'diningtable', 8: 'tvmonitor', 9: 'laptop', 10:
                                      'microwave', 11: 'refrigerator', 12: 'book', 13: 'clock', 14: 'vase', 15: 'gom'})
        df1_fur['like'] = 1


        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        style_result = mysql_controller.select_style1(filesrc)
        df1_style = pd.DataFrame(style_result)
        df1_style = df1_style.rename(columns={0: 'id', 1: 'img', 2: 'place', 3 : 'modern', 4: 'natural'})
        df1_style['like'] = 1


        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        color_result = mysql_controller.select_color1(filesrc)
        df1_color = pd.DataFrame(color_result)
        df1_color = df1_color.rename(columns={0: 'id', 1: 'img', 2: 'place', 3: 'Dark', 4: 'Deep blue', 5: 'Green', 6: 'Red', 7: 'Light blue', 8: 'purple', 9: 'Yellow', 10: 'White'})
        df1_color['like'] = 1


        abc = []
        abd = []
        abc1 = []
        abc2 = []
        for i in df1_fur['img']:
            if 'modern' in i:
                abc.append(i)
            if 'natural' in i:
                abd.append(i)

        for i in abc:
            if 'modern' in i:
                a = i.replace('modern', 'natural')
            abc1.append(a)

        for i in abd:
            if 'natural' in i:
                a = i.replace('natural', 'modern')
            abc2.append(a)

        ttt = []
        for i in abc1:
            ttt.append(i)
        for i in abc2:
            ttt.append(i)
        if len(ttt) != 10:
            for i in range(len(ttt),10):
                ttt.append(' ')

        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        result2 = mysql_controller.select_total2(ttt)
        df2_fur = pd.DataFrame(result2)
        df2_fur = df2_fur.rename(columns={0: 'id', 1: 'img', 2: 'place', 3: 'chair', 4: 'sofa', 5: 'pottedplant', 6:
            'bed', 7: 'diningtable', 8: 'tvmonitor', 9: 'laptop', 10:
                                    'microwave', 11: 'refrigerator', 12: 'book', 13: 'clock', 14: 'vase', 15: 'gom'})
        df2_fur['like'] = 0


        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        style_result2 = mysql_controller.select_style1(ttt)
        df2_style = pd.DataFrame(style_result2)
        df2_style = df2_style.rename(columns={0: 'id', 1: 'img', 2: 'place', 3 : 'modern', 4: 'natural'})
        df2_style['like'] = 0


        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        color_result2 = mysql_controller.select_color2(ttt)
        df2_color = pd.DataFrame(color_result2)
        df2_color = df2_color.rename(columns={0: 'id', 1: 'img', 2: 'place', 3: 'Dark', 4: 'Deep blue', 5: 'Green', 6: 'Red', 7: 'Light blue', 8: 'purple', 9: 'Yellow', 10: 'White'})
        df2_color['like'] = 0


        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        t1 = mysql_controller.select_total(filesrc)
        result3 = mysql_controller.select_total3(t1)

        df3_fur = pd.DataFrame(result3)
        df3_fur = df3_fur.rename(columns={0: 'id', 1: 'img', 2: 'place', 3: 'chair', 4: 'sofa', 5: 'pottedplant', 6:
            'bed', 7: 'diningtable', 8: 'tvmonitor', 9: 'laptop', 10:
                                      'microwave', 11: 'refrigerator', 12: 'book', 13: 'clock', 14: 'vase', 15: 'gom'})



        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        t2 = mysql_controller.select_total(filesrc)
        style_result3 = mysql_controller.select_style3(t2)

        df3_style = pd.DataFrame(style_result3)
        df3_style = df3_style.rename(columns={0: 'id', 1: 'img', 2: 'place', 3 : 'modern', 4: 'natural'})



        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        t3 = mysql_controller.select_total(filesrc)
        color_result3 = mysql_controller.select_color3(t3)

        df3_color = pd.DataFrame(color_result3)
        df3_color = df3_color.rename(columns={0: 'id', 1: 'img', 2: 'place', 3: 'Dark', 4: 'Deep blue', 5: 'Green', 6: 'Red', 7: 'Light blue', 8: 'purple', 9: 'Yellow', 10: 'White'})



        ##################################################################################################
        ######################## 모델 적용 ###############################################################

        ### 1) 데이터 준비

        # 데이터 준비 1 (rating data)
        df_web_style = pd.concat([df1_style, df2_style], ignore_index=True)
        df_web_fur = pd.concat([df1_fur, df2_fur], ignore_index=True)
        df_web_color = pd.concat([df1_color, df2_color], ignore_index=True)

        item_id = df_web_style['id']
        user_id = pd.Series(np.zeros(shape=(item_id.shape)))
        rating = df_web_style['like']

        df_merged = pd.DataFrame({'user_id': user_id, 'item_id': item_id, 'rating': rating})
        rating = pd.pivot_table(df_merged, values='rating', index=['item_id'], columns=['user_id'])

        # 데이터 준비 2 (웹 이미지 feature matrix)

        # df_style
        df_style = pd.DataFrame()
        for i in rating.index:
            a = df_web_style.loc[df_web_style['id'] == i].drop(columns=['img', 'place', 'like'])
            df_style = pd.concat([df_style, a])
        df_style = df_style.drop_duplicates(subset='id')
        df_style = df_style.set_index('id')

        # df_furniture
        df_furniture = pd.DataFrame()
        for i in rating.index:
            a = df_web_fur.loc[df_web_fur['id'] == i].drop(columns=['img', 'place', 'like'])
            df_furniture = pd.concat([df_furniture, a])
        df_furniture = df_furniture.drop_duplicates(subset='id')
        df_furniture = df_furniture.set_index('id')

        # df_color
        df_color = pd.DataFrame()
        for i in rating.index:
            a = df_web_color.loc[df_web_color['id'] == i].drop(columns=['img', 'place', 'like'])
            df_color = pd.concat([df_color, a])
        df_color = df_color.drop_duplicates(subset='id')
        df_color = df_color.set_index('id')

        # 데이터 준비 3 (추천 이미지 feature matrix)
        # df_new_style
        df_new_style = df3_style.drop(columns=['img', 'place'])
        df_new_style = df_new_style.set_index('id')
        # df_new_furniture
        df_new_furniture = df3_fur.drop(columns=['img', 'place'])
        df_new_furniture = df_new_furniture.set_index('id')
        # df_new_color
        df_new_color = df3_color.drop(columns=['img', 'place'])
        df_new_color = df_new_color.set_index('id')

        # ------------------------------------------
        ### 2) user profile 생성
        model = cbf_recommender(df_merged, rating)

        user_profile_style = model.get_user_profile(df_style, rating)
        user_profile_furniture = model.get_user_profile(df_furniture, rating)
        user_profile_color = model.get_user_profile(df_color, rating)

        # ------------------------------------------
        ### 3) 예측
        pred_by_style = model.predict(user_profile_style, df_new_style)
        pred_by_style = pred_by_style / pred_by_style.max()
        pred_by_furniture = model.predict(user_profile_furniture, df_new_furniture)
        pred_by_furniture = pred_by_furniture / pred_by_furniture.max()
        pred_by_color = model.predict(user_profile_color, df_new_color)
        pred_by_color = pred_by_color / pred_by_color.max()

        diff_style = pred_by_style.max() - pred_by_style.min()
        diff_furniture = pred_by_furniture.max() - pred_by_furniture.min()
        diff_color = pred_by_color.max() - pred_by_color.min()
        diff_sum = diff_style + diff_furniture + diff_color
        pred = (diff_style * pred_by_style + diff_furniture * pred_by_furniture + diff_color * pred_by_color) / diff_sum


        # ------------------------------------------
        ### 4) 예측
        user_no = 0
        top6 = model.recommend(pred, user_no).index
        top6 = list(top6)
        print(top6)

        mysql_controller = MysqlController('localhost', 'root', '1111!', 'final', 3306)
        ttt = mysql_controller.result_img(top6)

        totalttt = pd.DataFrame(ttt)
        totalttt = totalttt.rename(columns={0: 'img'})

        result_img_data = []
        for i in totalttt['img']:
            result_img_data.append(i)

        recommend_img1 = result_img_data[0]
        recommend_img2 = result_img_data[1]
        recommend_img3 = result_img_data[2]
        recommend_img4 = result_img_data[3]
        recommend_img5 = result_img_data[4]
        recommend_img6 = result_img_data[5]

        recommend_img1 = recommend_img1.replace('/MyHome/static/',"")

        recommend_img2 = recommend_img2.replace('/MyHome/static/', "")

        recommend_img3 = recommend_img3.replace('/MyHome/static/', "")

        recommend_img4 = recommend_img4.replace('/MyHome/static/', "")
        recommend_img5 = recommend_img5.replace('/MyHome/static/', "")
        recommend_img6 = recommend_img6.replace('/MyHome/static/', "")


        print(recommend_img1)
        print(recommend_img2)
        print(recommend_img3)
        print(recommend_img4)
        print(recommend_img5)
        print(recommend_img6)
    else:
        temp = None
    return render_template('result.html', src1=recommend_img1, src2=recommend_img2, src3=recommend_img3, src4=recommend_img4,src5=recommend_img5, src6 = recommend_img6)

@app.route('/second')
def second():
    return render_template('SecondPage.html')

@app.route('/finish')
def finish(src1 = None, src2 = None, src3 = None,src4 = None,src5 = None):
    return render_template('result.html', src1 = src1, src2 = src2, src3 = src3, src4 = src4, src5 = src5)



if __name__ == '__main__':
    app.run(host='1111',debug=True)




