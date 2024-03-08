
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List, Optional
from datetime import datetime
from fastapi.responses import JSONResponse
import os

# Secret key for JWT token
SECRET_KEY = os.getenv("SECRET_KEY", "secret")

# Algorithm used for JWT
ALGORITHM = "HS256"

# Define password context for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# User credentials model
class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

# Get user from database
def get_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user
async def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email, db)
    if user is None:
        raise credentials_exception
    return user


# Health check endpoint
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Login endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



































# from fastapi import APIRouter,Depends,status
# from fastapi.exceptions import HTTPException
# from fastapi_jwt_auth import AuthJWT
# from models import User,Order
# from schemas import OrderModel,OrderStatusModel
# from database import Session , engine
# from fastapi.encoders import jsonable_encoder

# order_router=APIRouter(
#     prefix="/orders",
#     tags=['orders']
# )


# session=Session(bind=engine)

# @order_router.get('/')
# async def hello(Authorize:AuthJWT=Depends()):

#     """
#         ## A sample hello world route
#         This returns Hello world
#     """

#     try:
#         Authorize.jwt_required()

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )
#     return {"message":"Hello World"}


# @order_router.post('/order',status_code=status.HTTP_201_CREATED)
# async def place_an_order(order:OrderModel,Authorize:AuthJWT=Depends()):
#     """
#         ## Placing an Order
#         This requires the following
#         - quantity : integer
#         - pizza_size: str
    
#     """


#     try:
#         Authorize.jwt_required()

#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )

#     current_user=Authorize.get_jwt_subject()

#     user=session.query(User).filter(User.username==current_user).first()


#     new_order=Order(
#         pizza_size=order.pizza_size,
#         quantity=order.quantity
#     )

#     new_order.user=user

#     session.add(new_order)

#     session.commit()


#     response={
#         "pizza_size":new_order.pizza_size,
#         "quantity":new_order.quantity,
#         "id":new_order.id,
#         "order_status":new_order.order_status
#     }

#     return jsonable_encoder(response)



    
# @order_router.get('/orders')
# async def list_all_orders(Authorize:AuthJWT=Depends()):
#     """
#         ## List all orders
#         This lists all  orders made. It can be accessed by superusers
        
    
#     """


#     try:
#         Authorize.jwt_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )

#     current_user=Authorize.get_jwt_subject()

#     user=session.query(User).filter(User.username==current_user).first()

#     if user.is_staff:
#         orders=session.query(Order).all()

#         return jsonable_encoder(orders)

#     raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="You are not a superuser"
#         )


# @order_router.get('/orders/{id}')
# async def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
#     """
#         ## Get an order by its ID
#         This gets an order by its ID and is only accessed by a superuser
        

#     """


#     try:
#         Authorize.jwt_required()
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )

#     user=Authorize.get_jwt_subject()

#     current_user=session.query(User).filter(User.username==user).first()

#     if current_user.is_staff:
#         order=session.query(Order).filter(Order.id==id).first()

#         return jsonable_encoder(order)

#     raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not alowed to carry out request"
#         )

    
# @order_router.get('/user/orders')
# async def get_user_orders(Authorize:AuthJWT=Depends()):
#     """
#         ## Get a current user's orders
#         This lists the orders made by the currently logged in users
    
#     """


#     try:
#         Authorize.jwt_required()
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )

#     user=Authorize.get_jwt_subject()


#     current_user=session.query(User).filter(User.username==user).first()

#     return jsonable_encoder(current_user.orders)


# @order_router.get('/user/order/{id}/')
# async def get_specific_order(id:int,Authorize:AuthJWT=Depends()):
#     """
#         ## Get a specific order by the currently logged in user
#         This returns an order by ID for the currently logged in user
    
#     """


#     try:
#         Authorize.jwt_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )

#     subject=Authorize.get_jwt_subject()

#     current_user=session.query(User).filter(User.username==subject).first()

#     orders=current_user.orders

#     for o in orders:
#         if o.id == id:
#             return jsonable_encoder(o)
    
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#         detail="No order with such id"
#     )


# @order_router.put('/order/update/{id}/')
# async def update_order(id:int,order:OrderModel,Authorize:AuthJWT=Depends()):
#     """
#         ## Updating an order
#         This udates an order and requires the following fields
#         - quantity : integer
#         - pizza_size: str
    
#     """

#     try:
#         Authorize.jwt_required()

#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

#     order_to_update=session.query(Order).filter(Order.id==id).first()

#     order_to_update.quantity=order.quantity
#     order_to_update.pizza_size=order.pizza_size

#     session.commit()


#     response={
#                 "id":order_to_update.id,
#                 "quantity":order_to_update.quantity,
#                 "pizza_size":order_to_update.pizza_size,
#                 "order_status":order_to_update.order_status,
#             }

#     return jsonable_encoder(order_to_update)

    
# @order_router.patch('/order/update/{id}/')
# async def update_order_status(id:int,
#         order:OrderStatusModel,
#         Authorize:AuthJWT=Depends()):


#     """
#         ## Update an order's status
#         This is for updating an order's status and requires ` order_status ` in str format
#     """
#     try:
#         Authorize.jwt_required()

#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

#     username=Authorize.get_jwt_subject()

#     current_user=session.query(User).filter(User.username==username).first()

#     if current_user.is_staff:
#         order_to_update=session.query(Order).filter(Order.id==id).first()

#         order_to_update.order_status=order.order_status

#         session.commit()

#         response={
#                 "id":order_to_update.id,
#                 "quantity":order_to_update.quantity,
#                 "pizza_size":order_to_update.pizza_size,
#                 "order_status":order_to_update.order_status,
#             }

#         return jsonable_encoder(response)


# @order_router.delete('/order/delete/{id}/',status_code=status.HTTP_204_NO_CONTENT)
# async def delete_an_order(id:int,Authorize:AuthJWT=Depends()):

#     """
#         ## Delete an Order
#         This deletes an order by its ID
#     """

#     try:
#         Authorize.jwt_required()

#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")


#     order_to_delete=session.query(Order).filter(Order.id==id).first()

#     session.delete(order_to_delete)

#     session.commit()

#     return order_to_delete





































# from fastapi import APIRouter,status,Depends
# from fastapi.exceptions import HTTPException
# from database import Session,engine
# from schemas import SignUpModel,LoginModel
# from models import User
# from fastapi.exceptions import HTTPException
# from werkzeug.security import generate_password_hash , check_password_hash
# from fastapi_jwt_auth import AuthJWT
# from fastapi.encoders import jsonable_encoder


# auth_router=APIRouter(
#     prefix='/auth',
#     tags=['auth']

# )


# session=Session(bind=engine)

# @auth_router.get('/')
# async def hello(Authorize:AuthJWT=Depends()):

#     """
#         ## Sample hello world route
    
#     """
#     try:
#         Authorize.jwt_required()

#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )

#     return {"message":"Hello World"}


# @auth_router.post('/signup',
#     status_code=status.HTTP_201_CREATED
# )
# async def signup(user:SignUpModel):
#     """
#         ## Create a user
#         This requires the following
#         ```
#                 username:int
#                 email:str
#                 password:str
#                 is_staff:bool
#                 is_active:bool

#         ```
    
#     """


#     db_email=session.query(User).filter(User.email==user.email).first()

#     if db_email is not None:
#         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with the email already exists"
#         )

#     db_username=session.query(User).filter(User.username==user.username).first()

#     if db_username is not None:
#         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with the username already exists"
#         )

#     new_user=User(
#         username=user.username,
#         email=user.email,
#         password=generate_password_hash(user.password),
#         is_active=user.is_active,
#         is_staff=user.is_staff
#     )

#     session.add(new_user)

#     session.commit()

#     return new_user



# #login route

# @auth_router.post('/login',status_code=200)
# async def login(user:LoginModel,Authorize:AuthJWT=Depends()):
#     """     
#         ## Login a user
#         This requires
#             ```
#                 username:str
#                 password:str
#             ```
#         and returns a token pair `access` and `refresh`
#     """
#     db_user=session.query(User).filter(User.username==user.username).first()

#     if db_user and check_password_hash(db_user.password, user.password):
#         access_token=Authorize.create_access_token(subject=db_user.username)
#         refresh_token=Authorize.create_refresh_token(subject=db_user.username)

#         response={
#             "access":access_token,
#             "refresh":refresh_token
#         }

#         return jsonable_encoder(response)

#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#         detail="Invalid Username Or Password"
#     )



# #refreshing tokens

# @auth_router.get('/refresh')
# async def refresh_token(Authorize:AuthJWT=Depends()):
#     """
#     ## Create a fresh token
#     This creates a fresh token. It requires an refresh token.
#     """


#     try:
#         Authorize.jwt_refresh_token_required()

#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Please provide a valid refresh token"
#         ) 

#     current_user=Authorize.get_jwt_subject()

    
#     access_token=Authorize.create_access_token(subject=current_user)

#     return jsonable_encoder({"access":access_token})

