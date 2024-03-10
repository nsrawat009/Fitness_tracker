from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_admin:Optional[bool]
    is_active:Optional[bool]
    

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"password",
                "is_admin":False,
                "is_active":True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key:str='b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'


class LoginModel(BaseModel):
    username:str
    password:str

class WorkoutResponseModel(BaseModel):
    id:Optional[int]
    date:Optional[str]
    user_id:Optional[int]
    exercise_name =str
    sets =int
    repetitions =Optional[int]
    weight_lifted =Optional[float]
    distance_covered =Optional[float]
    calories_burned =Optional[float]
    intensity_level =Optional[str]
    class Config:
         arbitrary_types_allowed = True
         schema_extra={
            'example':{
                "exercise_name":"PUSHUPS",
                "sets":3
            }
        }


# # Define ActivityCreate and other models here
# class ActivityCreate(BaseModel):
#     name: str
#     description: str
#     user_id: int

# class ActivityUpdate(BaseModel):
#     name: str
#     description: str

# class WorkoutCreate(BaseModel):
#     duration: int
#     user_id: int

# class WorkoutUpdate(BaseModel):
#     duration: int





















































# # from pydantic import BaseModel
# # from typing import Optional


# # class SignUpModel(BaseModel):
# #     id:Optional[int]
# #     username:str
# #     email:str
# #     password:str
# #     is_staff:Optional[bool]
# #     is_active:Optional[bool]


# #     class Config:
# #         orm_mode=True
# #         schema_extra={
# #             'example':{
# #                 "username":"johndoe",
# #                 "email":"johndoe@gmail.com",
# #                 "password":"password",
# #                 "is_staff":False,
# #                 "is_active":True
# #             }
# #         }



# # class Settings(BaseModel):
# #     authjwt_secret_key:str='b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'


# # class LoginModel(BaseModel):
# #     username:str
# #     password:str



# # class OrderModel(BaseModel):
# #     id:Optional[int]
# #     quantity:int
# #     order_status:Optional[str]="PENDING"
# #     pizza_size:Optional[str]="SMALL"
# #     user_id:Optional[int]


# #     class Config:
# #         orm_mode=True
# #         schema_extra={
# #             "example":{
# #                 "quantity":2,
# #                 "pizza_size":"LARGE"
# #             }
# #         }


# # class OrderStatusModel(BaseModel):
# #     order_status:Optional[str]="PENDING"

# #     class Config:
# #         orm_mode=True
# #         schema_extra={
# #             "example":{
# #                 "order_status":"PENDING"
# #             }
# #         }