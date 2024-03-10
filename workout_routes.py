from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User,Exercise
from schemas import WorkoutResponseModel
from database import Session , engine
from fastapi.encoders import jsonable_encoder

exercise_router=APIRouter(
    prefix="/exercises",
    tags=['exercises']
)


session=Session(bind=engine)

@exercise_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):

    """
        ## A sample hello world route
        This returns Hello world
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return {"message":"Hello World"}


@exercise_router.post('/exercise',status_code=status.HTTP_201_CREATED)
async def load_exercise(model:WorkoutResponseModel,Authorize:AuthJWT=Depends()):
    """
        ## Entering an exercise activity
        This requires the following
        - exercise_name : str
        - sets: int
    
    """


    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()


    new_exercise=Exercise(
        exercise_name=model.exercise_name,
        sets=model.sets
    )   

    new_exercise.user=user

    session.add(new_exercise)

    session.commit()


    response={
        "exercise_name":new_exercise.exercise_name,
        "sets":new_exercise.sets,
        "id":new_exercise.id,
    }

    return jsonable_encoder(response)



    
@exercise_router.get('/userdetails')
async def list_all_user_details(Authorize:AuthJWT=Depends()):
    """
        ## List all users details
        This lists all workout creations made by all users. It can be accessed by admin only
        
    
    """


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()

    if user.is_admin:
        orders=session.query(Exercise).all()

        return jsonable_encoder(orders)

    raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not an admin"
        )


@exercise_router.get('/userdetails/{id}')
async def get_user_details_by_id(id:int,Authorize:AuthJWT=Depends()):
    """
        ## Get user details by its ID
        This gets user details by its ID and is only accessed by admin
        

    """


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_admin:
        order=session.query(Exercise).filter(Exercise.id==id).first()

        return jsonable_encoder(order)

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not alowed to carry out request"
        )

    
@exercise_router.get('/user/userdetails')
async def get_user_details(Authorize:AuthJWT=Depends()):
    """
        ## Get the current user's workout details
        This lists the workout details made by the currently logged in users
    
    """


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()


    current_user=session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.userdetails)


@exercise_router.get('/user/userdetails/{id}/')
async def get_specific_userdetails(id:int,Authorize:AuthJWT=Depends()):
    """
        ## Get a specific order by the currently logged in user
        This returns an order by ID for the currently logged in user
    
    """


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    subject=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==subject).first()

    orders=current_user.userdetails

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="No user details with such id"
    )


@exercise_router.put('/exercise/update/{id}/')
async def update_user_details(id:int,model:WorkoutResponseModel,Authorize:AuthJWT=Depends()):
    """
        ## Updating user details
        This updates userdetails and requires the following fields
        - exercise_name : str
        - sets: int
    
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    exercise_to_update=session.query(Exercise).filter(Exercise.id==id).first()

    exercise_to_update.exercise_name=model.exercise_name
    exercise_to_update.sets=model.sets

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






# from schemas import ActivityResponse,WorkoutResponse
# from sqlalchemy.orm import sessionmaker, Session, relationship


# # Create new activity endpoint
# @app.post("/activities/", response_model=ActivityResponse)
# def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
#     new_activity = Activity(**activity.dict())
#     db.add(new_activity)
#     db.commit()
#     db.refresh(new_activity)
#     return new_activity

# # Retrieve all activities endpoint
# @app.get("/activities/", response_model=List[ActivityResponse])
# def get_activities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(Activity).offset(skip).limit(limit).all()

# # Retrieve activity by ID endpoint
# @app.get("/activities/{activity_id}", response_model=ActivityResponse)
# def get_activity(activity_id: int, db: Session = Depends(get_db)):
#     activity = db.query(Activity).filter(Activity.id == activity_id).first()
#     if activity is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
#     return activity

# # Update activity endpoint
# @app.put("/activities/{activity_id}", response_model=ActivityResponse)
# def update_activity(activity_id: int, activity_data: ActivityUpdate, db: Session = Depends(get_db)):
#     activity = db.query(Activity).filter(Activity.id == activity_id).first()
#     if activity is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
#     for key, value in activity_data.dict().items():
#         setattr(activity, key, value)
#     db.commit()
#     db.refresh(activity)
#     return activity

# # Delete activity endpoint
# @app.delete("/activities/{activity_id}")
# def delete_activity(activity_id: int, db: Session = Depends(get_db)):
#     activity = db.query(Activity).filter(Activity.id == activity_id).first()
#     if activity is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
#     db.delete(activity)
#     db.commit()
#     return