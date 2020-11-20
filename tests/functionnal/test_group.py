import uuid
import pytest
import json
from src.model import GroupModel, UserModel
from src import db

class TestGroup:

    ### CREATE GROUP ###

    def test_group_create_bad_jwt(self, test_client, headers_bad):
        """Test group creation with bad JWT token 

        Test:
            POST: /api/group

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.post("/api/group", headers=headers_bad, json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_group_create_fake_jwt(self, test_client, headers_fake):
        """Test group creation with fake JWT token 

        Test:
            POST: /api/group

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.post("/api/group", headers=headers_fake, json=dict(name="group_test"))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 404
        assert res['status'] == False

    def test_group_create_no_jwt(self, test_client):
        """Test group creation without JWT token 

        Test:
            POST: /api/group

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post("/api/group", json=dict(name="group_test"))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header" 

    def test_group_create(self, test_client, headers):
        """Test group creation

        Test:
            POST: /api/group

        Expected result: 
            201, {"status": True, "group": GroupObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.post("/api/group", headers=headers, json=dict(name="group_test"))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(name="group_test").first()

        assert response.status_code == 201
        assert res['status'] == True
        assert res['group']['name'] == group.name
        assert res['group']['name'] == "group_test"

    ### GROUP RESOURCE ###

    def test_group_get_id_bad_jwt(self, test_client, headers_bad, group_test):
        """Test group by id with bad JWT token  

        Test:
            GET: /api/group/<group_id>

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
            group_test (Group object): group test
        """
        response = test_client.get("/api/group/"+str(group_test.group_id), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_group_get_id_no_jwt(self, test_client, group_test):
        """Test group by id without JWT token  

        Test:
            GET: /api/group/<group_id>

        Expected result: 
            401, {"msg": "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
            group_test (Group object): group test
        """
        response = test_client.get("/api/group/"+str(group_test.group_id))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_group_get_id_bad_group_id(self, test_client, headers):
        """Test group by id with bad id

        Test:
            GET: /api/group/<bad_group_id>

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/group/"+str(9999999), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_group_get_id(self, test_client, headers, group_test):
        """Test group by id

        Test:
            GET: /api/group/<group_id>

        Expected result: 
            201, {"status": True, "group": GroupObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            group_test (Group object): group test
        """
        response = test_client.get("/api/group/"+str(group_test.group_id), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['group']['name'] == group_test.name
        assert res['group']['name'] == "group_test"

    ### GROUP INVITATIONS ###

    def test_group_invitation_bad_group_id(self, test_client, headers, user_test2, group_test):
        """Test group invitation with bad group id

        Test:
            POST: /api/group/<bad_group_id>/invitations

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test2 (User object): user test 2
            group_test (Group object): group test
        """
        response = test_client.post("/api/group/"+str(9999999)+"/invitations", headers=headers, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_group_invitation_bad_owner_group_id(self, test_client, headers, user_test2, group_test2):
        """Test group invitation send from no group owner

        Test:
            POST: /api/group/<bad_group_id>/invitations

        Expected result: 
            403, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test2 (User object): user test 2
            group_test2 (Group object): group test 2
        """
        response = test_client.post("/api/group/"+str(group_test2.group_id)+"/invitations", headers=headers, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(group_id=group_test2.group_id).first()

        assert response.status_code == 403
        assert res['status'] == False
        assert user_test2 not in group.invitations
    
    def test_group_invitation_bad_jwt(self, test_client, headers_bad, user_test2):
        """Test group invitation with bad JWT token

        Test:
            POST: /api/group/<group_id>/invitations

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
            user_test2 (User object): user test 2
        """
        response = test_client.post("/api/group/"+str(9999999)+"/invitations", headers=headers_bad, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_group_invitation_fake_jwt(self, test_client, headers_fake, user_test2):
        """Test group invitation with fake JWT token

        Test:
            POST: /api/group/<group_id>/invitations

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
            user_test2 (User object): user test 2
        """
        response = test_client.post("/api/group/"+str(9999999)+"/invitations", headers=headers_fake, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_group_invitation(self, test_client, headers, user_test2, group_test):
        """Test group invitation 

        Test:
            POST: /api/group/<group_id>/invitations

        Expected result: 
            202, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test2 (User object): user test 2
            group_test (Group object): group test
        """
        response = test_client.post("/api/group/"+str(group_test.group_id)+"/invitations", headers=headers, json=dict(
            uuid=user_test2.uuid
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(group_id=group_test.group_id).first()

        assert response.status_code == 200
        assert res['status'] == True
        assert user_test2 in group.invitations
    
    def test_group_invitation_already_invited(self, test_client, headers, user_test2, group_test):
        """Test group invitation user already invited

        Test:
            POST: /api/group/<group_id>/invitations

        Expected result: 
            400, {"status": False, "message": "Invitation already sended !"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test2 (User object): user test 2
            group_test (Group object): group test
        """
        response = test_client.post("/api/group/"+str(group_test.group_id)+"/invitations", headers=headers, json=dict(
            uuid=str(user_test2.uuid)
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(group_id=group_test.group_id).first()

        assert response.status_code == 400
        assert res['status'] == False
        assert res["message"] == "Invitation already sended !"
        assert user_test2 in group.invitations

    def test_group_invitation_already_member(self, test_client, headers, user_test2, group_test):
        """Test group invitation user already member

        Test:
            POST: /api/group/<bad_group_id>/invitations

        Expected result: 
            400, {"status": False, "message": "User is already a member of this group !"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test2 (User object): user test 2
            group_test (Group object): group test
        """
        if (user_test2 in group_test.invitations):
            group_test.invitations.remove(user_test2)
        group_test.members.append(user_test2)
        db.session.add(group_test)
        db.session.commit()
        response = test_client.post("/api/group/"+str(group_test.group_id)+"/invitations", headers=headers, json=dict(
            uuid=str(user_test2.uuid)
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(group_id=group_test.group_id).first()

        assert response.status_code == 400
        assert res['status'] == False
        assert res['message'] == "User is already a member of this group !"
        assert user_test2 in group.members

    def test_group_invitation_owner_invite_itself(self, test_client, headers, user_test1, group_test):
        """Test group invitation owner invite itself

        Test:
            POST: /api/group/<group_id>/invitations

        Expected result: 
            400, {"status": False, "message": "You can not invite yourself to your group !"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test 1
            group_test (Group object): group test
        """
        response = test_client.post("/api/group/"+str(group_test.group_id)+"/invitations", headers=headers, json=dict(
            uuid=str(user_test1.uuid)
            ))
        res = json.loads(response.data)
        group = GroupModel.query.filter_by(group_id=group_test.group_id).first()

        assert response.status_code == 400
        assert res['status'] == False
        assert res['message'] == "You can not invite yourself to your group !"
    
    def test_group_invitation_no_jwt(self, test_client, user_test2, group_test):
        """Test group invitation without JWT token

        Test:
            POST: /api/group/<group_id>/invitations

        Expected result: 
            401, {"status": False, "msg": "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
            user_test2 (User object): user test 2
            group_test (Group object): group test
        """
        response = test_client.post("/api/group/"+str(group_test.group_id)+"/invitations", json=dict(
            uuid=str(user_test2.uuid)
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### GROUP ACCEPT INVITATION USER ###

    def test_group_accept_invitation_bad_group(self, test_client, headers, user_test1, user_test2):
        """Test group accept invitation from bad group

        Test:
            PUT: /api/group/<bad_group_id>/invitations/<user_uuid>

        Expected result: 
            404, {"status": False, "message": "Group not found!"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test 1
            user_test2 (User object): user test 2
        """
        response = test_client.put("/api/group/"+str(99999)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Group not found!"

    def test_group_accept_invitation_bad_jwt(self, test_client, headers_bad, user_test1, group_test2):
        """Test group accept invitation with bad JWT token

        Test:
            PUT: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        response = test_client.put("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422
        
    def test_group_accept_invitation_fake_jwt(self, test_client, headers_fake, user_test1, group_test2):
        """Test group accept invitation with fake JWT token

        Test:
            PUT: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            404, {"status": False, "message": "Member not found!"}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        response = test_client.put("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Member not found!"

    def test_group_accept_invitation_no_jwt(self, test_client, user_test1, group_test2):
        """Test group accept invitation without JWT token

        Test:
            PUT: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            401, {"status": False, "message": "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        response = test_client.put("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_group_accept_invitation_other_user(self, test_client, headers, user_test2, group_test2):
        """Test group accept invitation not intended to the user

        Test:
            PUT: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            403, {"status": False, "message": "Unable to accept an invitation that is not intended to you"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test2 (User object): user test 2
            group_test2 (Group object): group test 2
        """
        response = test_client.put("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test2.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False
        assert res['message'] == "Unable to accept an invitation that is not intended to you"

    def test_group_accept_invitation_no_invitation(self, test_client, headers, user_test1, group_test2):
        """Test group accept nonexistent invitation

        Test:
            PUT: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            404, {"status": False, "message": "Invitation not found !"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        if(user_test1 in group_test2.members):
            group_test2.members.remove(user_test1)
        if (user_test1 in group_test2.invitations):
            group_test2.invitations.remove(user_test1)
        db.session.add(group_test2)
        db.session.commit()
        response = test_client.put("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Invitation not found !"
    
    def test_group_accept_invitation(self, test_client, headers, user_test1, group_test2):
        """Test group accept invitation

        Test:
            PUT: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            200, {"status": True, "message": "Member add to group", "group": GroupObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        if(user_test1 in group_test2.members):
            group_test2.members.remove(user_test1)
        if (user_test1 not in group_test2.invitations):
            group_test2.invitations.append(user_test1)
        db.session.add(group_test2)
        db.session.commit()
        response = test_client.put("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['message'] == "Member add to group"
        assert user_test1.username in res["group"]["members"][0]["username"]

    ### GROUP DELETE INVITATION USER ###

    def test_group_delete_invitation_bad_group(self, test_client, headers, user_test1, user_test2):
        """Test group delete invitation with bad group id

        Test:
            DELETE: /api/group/<bad_group_id>/invitations/<user_uuid>

        Expected result: 
            404, {"status": False, "message": "Group not found!"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test 1
            user_test2 (User object): user test 2
        """
        response = test_client.delete("/api/group/"+str(99999)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Group not found!"

    def test_group_delete_invitation_bad_jwt(self, test_client, headers_bad, user_test1, group_test2):
        """Test group delete invitation with bad JWT token

        Test:
            DELETE: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): fake HTTP header, with invalid signed access token
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        response = test_client.delete("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422
        
    def test_group_delete_invitation_fake_jwt(self, test_client, headers_fake, user_test1, group_test2):
        """Test group delete invitation with fake JWT token

        Test:
            DELETE: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            404, {"status": False, "message": "Member not found!"}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        response = test_client.delete("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Member not found!"

    def test_group_delete_invitation_no_jwt(self, test_client, user_test1, group_test2):
        """Test group delete invitation with fake JWT token

        Test:
            DELETE: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            401, {"msg": "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        response = test_client.delete("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_group_delete_invitation_other_user(self, test_client, headers, user_test2, group_test2):
        """Test group delete invitation beloging to another user

        Test:
            DELETE: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            403, {"status": False, "message": "Unable to delete an invitation that is not intended to you if you are not the group owner"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test2 (User object): user test 2
            group_test2 (Group object): group test 2
        """
        response = test_client.delete("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test2.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False
        assert res['message'] == "Unable to delete an invitation that is not intended to you if you are not the group owner"

    def test_group_delete_invitation_no_invitation(self, test_client, headers, user_test1, group_test2):
        """Test group delete nonexistent invitation

        Test:
            DELETE: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            404, {"status": False, "message": "Invitation not found !"}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        if(user_test1 in group_test2.members):
            group_test2.members.remove(user_test1)
        if (user_test1 in group_test2.invitations):
            group_test2.invitations.remove(user_test1)
        db.session.add(group_test2)
        db.session.commit()
        response = test_client.delete("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
        assert res['message'] == "Invitation not found !"
    
    def test_group_delete_invitation(self, test_client, headers, user_test1, group_test2):
        """Test group delete invitation

        Test:
            DELETE: /api/group/<group_id>/invitations/<user_uuid>

        Expected result: 
            204

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test 1
            group_test2 (Group object): group test 2
        """
        if(user_test1 in group_test2.members):
            group_test2.members.remove(user_test1)
        if (user_test1 not in group_test2.invitations):
            group_test2.invitations.append(user_test1)
        db.session.add(group_test2)
        db.session.commit()
        response = test_client.delete("/api/group/"+str(group_test2.group_id)+"/invitations/"+str(user_test1.uuid), headers=headers)
        res = response.data

        assert response.status_code == 204
        assert res == b''

    ### DELETE/LEAVE GROUP ###

    def test_group_delete_bad_group_id(self, test_client, headers):
        """Test group delete group with bad id

        Test:
            DELETE: /api/group/<bad_group_id>

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.delete("/api/group/"+str(999999), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_group_delete_fake_jwt(self, test_client, headers_fake, group_test):
        """Test group delete group with fake JWT token

        Test:
            DELETE: /api/group/<group_id>

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
            group_test (Group object): group test
        """
        response = test_client.delete("/api/group/"+str(group_test.group_id), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_group_delete_bad_jwt(self, test_client, headers_bad, group_test):
        """Test group delete group with bad JWT token

        Test:
            DELETE: /api/group/<group_id>

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
            group_test (Group object): group test
        """
        response = test_client.delete("/api/group/"+str(group_test.group_id), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_group_delete_no_jwt(self, test_client, group_test):
        """Test group delete group without JWT token

        Test:
            DELETE: /api/group/<group_id>

        Expected result: 
            401, {"msg": "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
            group_test (Group object): group test
        """
        response = test_client.delete("/api/group/"+str(group_test.group_id))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_group_leave(self, test_client, headers, user_test2, group_test2):
        """Test group leave group

        Test:
            DELETE: /api/group/<group_id>

        Expected result: 
            204

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test2 (User object): user test 2
            group_test2 (Group object): group test 2
        """
        user = UserModel.query.filter_by(username="test").first()
        if user not in group_test2.members:
            group_test2.members.append(user)
        db.session.add(group_test2)
        db.session.commit()

        response = test_client.delete("/api/group/"+str(group_test2.group_id), headers=headers, json=dict(name="group_test"))
        res = response.data
        group = GroupModel.query.filter_by(group_id=group_test2.group_id).first()

        assert response.status_code == 204
        assert res == b""
        assert user not in group.members
    
    def test_group_delete(self, test_client, headers, group_test):
        """Test group delete group

        Test:
            DELETE: /api/group/<group_id>

        Expected result: 
            204

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            group_test (Group object): group test 
        """
        response = test_client.delete("/api/group/"+str(group_test.group_id), headers=headers, json=dict(name="group_test"))
        res = response.data
        group = GroupModel.query.filter_by(group_id=group_test.group_id).first()

        assert response.status_code == 204
        assert res == b""
        assert group == None