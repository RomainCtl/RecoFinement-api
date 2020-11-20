import uuid
import pytest
import json
from src.model import GroupModel, UserModel
from src import db

class TestGroup:

    ### CREATE GROUP ###

    def test_group_create_bad_jwt(self, test_client, headers_bad):
        response = test_client.post("/api/group", headers=headers_bad, json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_group_create_fake_jwt(self, test_client, headers_fake):
        response = test_client.post("/api/group", headers=headers_fake, json=dict(name="group_test"))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 404
        assert res['status'] == False

    def test_group_create_no_jwt(self, test_client):
        response = test_client.post("/api/group", json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header" 

    def test_group_create(self, test_client, headers):
        response = test_client.post("/api/group", headers=headers, json=dict(name="group_test"))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 201
        assert res['status'] == True
        assert res['group']['name'] == group.name
        assert res['group']['name'] == "group_test"

    ### GROUP RESOURCE ###

    def test_group_get_id_bad_jwt(self, test_client, headers_bad):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.get("/api/group/"+str(group.group_id), headers=headers_bad, json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_group_get_id_no_jwt(self, test_client):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.get("/api/group/"+str(group.group_id), json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_group_get_id_bad_group_id(self, test_client, headers):
        response = test_client.get("/api/group/"+str(9999999), headers=headers, json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_group_get_id(self, test_client, headers):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.get("/api/group/"+str(group.group_id), headers=headers, json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['group']['name'] == group.name
        assert res['group']['name'] == "group_test"

    ### GROUP INVITATIONS ###

    def test_group_invitation_bad_group_id(self, test_client, headers, user_test2):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.post("/api/group/"+str(9999999)+"/invitations", headers=headers, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 404
        assert res['status'] == False
        assert user_test2 not in group.invitations

    def test_group_invitation_bad_owner_group_id(self, test_client, headers, user_test2):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.post("/api/group/"+str(group.group_id)+"/invitations", headers=headers, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 403
        assert res['status'] == False
        assert user_test2 not in group.invitations
    
    def test_group_invitation_bad_jwt(self, test_client, headers_bad, user_test2):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.post("/api/group/"+str(9999999)+"/invitations", headers=headers_bad, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_group_invitation_fake_jwt(self, test_client, headers_fake, user_test2):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.post("/api/group/"+str(9999999)+"/invitations", headers=headers_fake, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_group_invitation(self, test_client, headers, user_test2):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.post("/api/group/"+str(group.group_id)+"/invitations", headers=headers, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 200
        assert res['status'] == True
        assert user_test2 in group.invitations
    
    def test_group_invitation_already_invited(self, test_client, headers, user_test2):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.post("/api/group/"+str(group.group_id)+"/invitations", headers=headers, json=dict(
            uuid=str(user_test2.uuid)
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 400
        assert res['status'] == False
        assert res["message"] == "Invitation already sended !"
        assert user_test2 in group.invitations

    def test_group_invitation_already_member(self, test_client, headers, user_test2):
        group = GroupModel.query.filter_by(name="group_test").first()
        if (user_test2 in group.invitations):
            group.invitations.remove(user_test2)
        group.members.append(user_test2)
        db.session.add(group)
        db.session.commit()
        response = test_client.post("/api/group/"+str(group.group_id)+"/invitations", headers=headers, json=dict(
            uuid=str(user_test2.uuid)
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 400
        assert res['status'] == False
        assert res['message'] == "User is already a member of this group !"
        assert user_test2 in group.members

    def test_group_invitation_owner_invite_itself(self, test_client, headers, user_test1):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.post("/api/group/"+str(group.group_id)+"/invitations", headers=headers, json=dict(
            uuid=str(user_test1.uuid)
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 400
        assert res['status'] == False
        assert res['message'] == "You can not invite yourself to your group !"
    
    def test_group_invitation_no_jwt(self, test_client, user_test2):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.post("/api/group/"+str(group.group_id)+"/invitations", json=dict(
            uuid=str(user_test2.uuid)
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### GROUP INVITATION USER ###

    def test_group_accept_invitation_bad_group(self, test_client, headers, user_test1, user_test2):
        response = test_client.put("/api/group/"+str(99999)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Group not found!"

    def test_group_accept_invitation_bad_jwt(self, test_client, headers_bad, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.put("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422
        
    def test_group_accept_invitation_fake_jwt(self, test_client, headers_fake, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.put("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Member not found!"

    def test_group_accept_invitation_no_jwt(self, test_client, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.put("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_group_accept_invitation_other_user(self, test_client, headers, user_test2):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.put("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test2.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False
        assert res['message'] == "Unable to accept an invitation that is not intended to you"

    def test_group_accept_invitation_no_invitation(self, test_client, headers, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        if(user_test1 in group.members):
            group.members.remove(user_test1)
        if (user_test1 in group.invitations):
            group.invitations.remove(user_test1)
        db.session.add(group)
        db.session.commit()
        response = test_client.put("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Invitation not found !"
    
    def test_group_accept_invitation(self, test_client, headers, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        if(user_test1 in group.members):
            group.members.remove(user_test1)
        if (user_test1 not in group.invitations):
            group.invitations.append(user_test1)
        db.session.add(group)
        db.session.commit()
        response = test_client.put("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['message'] == "Member add to group"
        assert user_test1.username in res["group"]["members"][0]["username"]

    ### GROUP DELETE INVITATION USER ###

    def test_group_delete_invitation_bad_group(self, test_client, headers, user_test1, user_test2):
        response = test_client.delete("/api/group/"+str(99999)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Group not found!"

    def test_group_delete_invitation_bad_jwt(self, test_client, headers_bad, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.delete("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422
        
    def test_group_delete_invitation_fake_jwt(self, test_client, headers_fake, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.delete("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Member not found!"

    def test_group_delete_invitation_no_jwt(self, test_client, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.delete("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_group_delete_invitation_other_user(self, test_client, headers, user_test2):
        group = GroupModel.query.filter_by(name="group_test2").first()
        response = test_client.delete("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test2.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False
        assert res['message'] == "Unable to delete an invitation that is not intended to you if you are not the group owner"

    def test_group_delete_invitation_no_invitation(self, test_client, headers, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        if(user_test1 in group.members):
            group.members.remove(user_test1)
        if (user_test1 in group.invitations):
            group.invitations.remove(user_test1)
        db.session.add(group)
        db.session.commit()
        response = test_client.delete("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Invitation not found !"
    
    def test_group_delete_invitation(self, test_client, headers, user_test1):
        group = GroupModel.query.filter_by(name="group_test2").first()
        if(user_test1 in group.members):
            group.members.remove(user_test1)
        if (user_test1 not in group.invitations):
            group.invitations.append(user_test1)
        db.session.add(group)
        db.session.commit()
        response = test_client.delete("/api/group/"+str(group.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = response.data

        assert response.status_code == 204
        assert res == b''

    ### DELETE/LEAVE GROUP ###

    def test_group_delete_bad_group_id(self, test_client, headers):
        response = test_client.delete("/api/group/"+str(999999), headers=headers, json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_group_delete_fake_jwt(self, test_client, headers_fake):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.delete("/api/group/"+str(group.group_id), headers=headers_fake, json=dict(name="group_test"))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_group_delete_bad_jwt(self, test_client, headers_bad):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.delete("/api/group/"+str(group.group_id), headers=headers_bad, json=dict(name="group_test"))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 422

    def test_group_delete_no_jwt(self, test_client):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.delete("/api/group/"+str(group.group_id), json=dict(name="group_test"))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_group_leave(self, test_client, headers, user_test2):
        new_group = GroupModel(
            name="group_test2",
            owner_id = user_test2.user_id
            )
        db.session.add(new_group)
        db.session.commit()
        group = GroupModel.query.filter_by(name="group_test2").first()
        user = UserModel.query.filter_by(username="test").first()
        if user not in group.members:
            group.members.append(user)
        db.session.add(group)
        db.session.commit()

        response = test_client.delete("/api/group/"+str(group.group_id), headers=headers, json=dict(name="group_test"))
        res = response.data
        group = GroupModel.query.filter_by(name="group_test2").first()

        assert response.status_code == 204
        assert res == b""
        assert user not in group.members
    
    def test_group_delete(self, test_client, headers):
        group = GroupModel.query.filter_by(name="group_test").first()
        response = test_client.delete("/api/group/"+str(group.group_id), headers=headers, json=dict(name="group_test"))
        res = response.data
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 204
        assert res == b""
        assert group == None