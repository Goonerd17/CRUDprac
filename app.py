from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.qrfh6ue.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

#Member Create
@app.route("/member", methods=["POST"])
def member_post():
    name_receive = request.form["name_give"]
    
    doc = {
        'name':name_receive,
    }  
    
    db.members.insert_one(doc)
    
    return jsonify({'msg': '저장 성공'})



#Member Read
@app.route("/member", methods=["GET"])
def member_get():
    name = request.args.get('name') # args.get는 Flask에서 GET 요청의 ? 쿼리 매개변수(Query Parameter) ?를 가져오는 메서드

    member = db.members.find_one({'name':name})

    if member:                      # if 문에 대해서 좀 더 자세히 알 필요가 있음
        member['_id'] = str(member['_id'])
        return jsonify({'result': member})
    else:
        return jsonify({'result': None})



"""
이 부분은 수정 후, 수정되었다는 알림만을 전송할 때 사용. index.html update2_member 함수를 찾아 확인 해볼 것
Member Update
@app.route("/member", methods=["PUT"])
def member_put():
    data = request.get_json()      # 클라이언트로부터 전달받은 JSON 데이터 가져오기
    name = data.get('name')        # 수정할 이름 가져오기
    newName = data.get('newName')  # 새 이름 가져오기
    
    result = db.members.update_one({'name': name}, {'$set': {'name': newName}}) # 데이터베이스에서 해당 이름을 찾아 업데이트

    if result.modified_count > 0:
        return jsonify({'message': '이름이 수정되었습니다.'})
    else:
        return jsonify({'message': '이름 수정에 실패했습니다.'})
"""        

# Member Update
@app.route("/member", methods=["PUT"])
def member_put():
    name = request.json.get('name')
    new_name = request.json.get('newName')
   
    member = db.members.update_one({'name': name}, {'$set': {'name': new_name}}) # 수정 작업
    member = db.members.find_one({'name': new_name})                             # 다시 찾기

    if member:
        member['_id'] = str(member['_id'])
        return jsonify({'result': member})
    else:
        return jsonify({'result': None})



#Member Delete
@app.route("/member/delete", methods=["DELETE"])
def member_delete():
    name = request.json['name']   # 요청 바디에서 삭제할 이름을 가져옴.

    result = db.members.delete_one({'name': name})

    if result.deleted_count > 0:  # .deleted_count
        return jsonify({'message': '삭제 성공'})
    else:
        return jsonify({'message': '삭제 실패'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)