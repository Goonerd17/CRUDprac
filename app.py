from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.qrfh6ue.mongodb.net/?retryWrites=true&w=majority') 
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')





#Member Create, POST
@app.route("/member", methods=["POST"])
def member_post():
    name_receive = request.form["name_give"] # 추가된 이름
    
    doc = {
        'name':name_receive,
    }  
    
    db.members.insert_one(doc)               # 데이터베이스에 저장
    
    return jsonify({'msg': '저장 성공'})      # '저장성공'이라는 값을 가진 msg를 return




#Member Read, GET
@app.route("/member", methods=["GET"])
def member_get():
    name = request.args.get('name')             # args.get는 Flask에서 GET 요청의 쿼리 매개변수를 가져오는 메서드. 쿼리 매개변수 = URL 뒷부분에 물음표를 사용하여 전달되는 매개변수. 여러 개의 매개변수는 &로 구분 

    member = db.members.find_one({'name':name}) # 데이터베이스에서 검색

    if member:                           
        member['_id'] = str(member['_id'])      # 조회한 member객체의 _id 필드 값을 문자열로 변환하여 다시 id에 할당, MongoDB에서는 일반적으로 ObjectId 형식으로 저장되지만 JSON으로 응답할 때에는 문자열 형태로 변환해야함
        return jsonify({'result': member})
    else:
        return jsonify({'result': None})        # 데이터베이스에서 요청받은 name을 가진 member가 존재한다면 member값을 가진 result 반환, 존재하지 않다면 None 반환 




"""
이 부분은 수정 후, 수정되었다는 알림만을 전송할 때 사용. index.html update2_member 함수를 찾아 확인 해볼 것
Member Update
@app.route("/member", methods=["PUT"])
def member_put():
    data = request.get_json()      
    name = data.get('name')        
    newName = data.get('newName') 
    
    result = db.members.update_one({'name': name}, {'$set': {'name': newName}}) 

    if result.modified_count > 0:
        return jsonify({'message': '이름이 수정되었습니다.'})
    else:
        return jsonify({'message': '이름 수정에 실패했습니다.'})
"""        

# Member Update, PUT
@app.route("/member", methods=["PUT"])
def member_put():
    name = request.json.get('name')         # 수정할 이름 가져오기
    new_name = request.json.get('newName')  # 새 이름 가져오기
   
    member = db.members.update_one({'name': name}, {'$set': {'name': new_name}}) # 데이터베이스에서 해당 이름을 찾아 업데이트
    member = db.members.find_one({'name': new_name})                             # 수정된 이름 검색

    if member:
        member['_id'] = str(member['_id'])
        return jsonify({'result': member})
    else:
        return jsonify({'result': None})




#Member Delete, DELETE
@app.route("/member/delete", methods=["DELETE"])
def member_delete():
    name = request.json['name']                      # 삭제할 이름을 가져옴.

    result = db.members.delete_one({'name': name})   # 데이터베이스에서 해당 이름을 가진 데이터 삭제

    if result.deleted_count > 0:                     # .deleted_count = 삭제된 횟수, 0 아니면 1의 값을 가짐
        return jsonify({'message': '삭제 성공'})
    else:
        return jsonify({'message': '삭제 실패'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)