

# class Admin(Resource):
#     @cross_origin()
#     @jwt_required()
#     def get(self):
#         try:
#             current_user_id = get_jwt_identity()
#             current_user = User.query.get(current_user_id)
            
#             if not isinstance(current_user, User) or not current_user.is_banda_admin:
#                 return jsonify({'message': 'Unauthorized access'}), 403
                
#             all_users = User.query.all()
            
#             serialized_users = [user.to_dict() for user in all_users]
            
#             return jsonify(serialized_users), 200
            
#         except Exception as e:
#             return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
      


# class UserDetailsAdmin(Resource):
#     @jwt_required()
#     @cross_origin() 
#     def get(self, user_id):
#         try:
#             current_user_id = get_jwt_identity()
#             current_user = db.session.get(User, current_user_id)
            
#             if not current_user or not current_user.is_banda_admin:
#                 return jsonify({'message': 'Access Denied, Admin privileges required'}), 403
            
#             target_user = db.session.get(User, user_id)
#             if not target_user:
#                 return jsonify({'message': 'User not found'}), 404
            
#             return jsonify(target_user.to_dict()), 200
#         except Exception as e:
#             return jsonify({'message': str(e)}), 500

#     @jwt_required()
#     @cross_origin() 
#     def put(self, user_id):
#         try:
#             current_user_id = get_jwt_identity()
#             current_user = db.session.get(User, current_user_id)
            
#             if not current_user or not current_user.is_banda_admin:
#                 return jsonify({'message': 'Access Denied, Admin privileges required'}), 403
            
#             target_user = db.session.get(User, user_id)
#             if not target_user:
#                 return jsonify({'message': 'User not found'}), 404
            
#             data = request.json
#             if 'username' in data:
#                 target_user.username = data['username']
#             if 'email' in data:
#                 target_user.email = data['email']
#             if 'location' in data:
#                 target_user.location = data['location']
#             if 'contact' in data:
#                 target_user.contact = data['contact']
#             if 'role' in data:
#                 target_user.role = data['role']
#             if 'is_banda_admin' in data:
#                 target_user.is_banda_admin = data['is_banda_admin']
#             if 'is_banda_delivery' in data:
#                 target_user.is_banda_delivery = data['is_banda_delivery']

#             db.session.commit()
#             return jsonify({'message': 'User updated successfully'}), 200
#         except Exception as e:
#             return jsonify({'message': str(e)}), 500

#     @jwt_required()
#     @cross_origin() 
#     def delete(self, user_id):
#         try:
#             current_user_id = get_jwt_identity()
#             current_user = db.session.get(User, current_user_id)
            
#             if not current_user or not current_user.is_banda_admin:
#                 return jsonify({'message': 'Access Denied, Admin privileges required'}), 403
            
#             target_user = db.session.get(User, user_id)
#             if not target_user:
#                 return jsonify({'message': 'User not found'}), 404
            
#             db.session.delete(target_user)
#             db.session.commit()
#             return jsonify({'message': 'User deleted successfully'}), 200
#         except Exception as e:
#             return jsonify({'message': str(e)}), 500
