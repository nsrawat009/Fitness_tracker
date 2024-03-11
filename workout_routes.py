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
        ## Updating exercise details
        This updates exercise details and requires the following fields
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

    session.commit()


    response={
                "exercise_name":exercise_to_update.exercise_name,
                "sets":exercise_to_update.sets,
              
               
            }

    return jsonable_encoder(exercise_to_update)

    

@exercise_router.delete('/exercise/delete/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_exercise_details(id:int,Authorize:AuthJWT=Depends()):

    """
        ## Delete exercise details
        This deletes exercise details by its ID
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")


    exercise_to_delete=session.query(Exercise).filter(Exercise.id==id).first()

    session.delete(exercise_to_delete)

    session.commit()

    return exercise_to_delete





