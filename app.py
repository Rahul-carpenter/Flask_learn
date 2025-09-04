from flask import Flask, request, render_template

app=Flask(__name__)

@app.get("/")
def home():
    return "Home page"

# @app.get("/welcome")
# def welcome():
#     user=request.args.get("user","guest")
#     return render_template("welcome.html", title="Welcome Page", user=user)

# @app.get("/hello/<name>")
# def hello_name(name):
#     return f"Hello {name}"

# @app.get("/greet/<user>/<int:age>")
# def greet(user,age):
#     return f"Hello {user} you are {age} years old"

# @app.get("/cube/<int:n>")
# def cube(n):
#     return {"cube": n**3}

# @app.get("/add")
# def add():
#     a=request.args.get("a",type=int, default=0)
#     b=request.args.get("b",type=int, default=0)
#     return {"a": a, "b":b, "Sum": a+b}


#  Post routes
users=[]
@app.post("/signup")
def signup():
    data=request.get_json()
    user_name= data.get("username")
    email=data.get("Email")
    user_password=data.get("password")

    for u in users:
        if u["username"]==user_name:
            return {"Meassage":"User already exist"},400
        
    user={"username":user_name,"Email":email,"Pasword":user_password}
    users.append(user)

    return {"meassage":f"User {user_name} ragister suscessfully"}


@app.post("/login")
def login():
    data=request.get_json()
    user_name= data.get("username")
    user_password=data.get("password")

    if user_name=="admin" and user_password=="admin123":
        return {"message":f"Welcome {user_name}"}
   
    return {"msg":f'Enter correct details'},401

@app.get("/users")
def get():
    return {"Users":users}


#    Put routes (update)

@app.put("/users/<user_name>")
def update_user(user_name):
    data=request.get_json()
    for u in users:
        if u["username"]==user_name:
            u["Email"]=data.get("Email",u["Email"])
            u["Pasword"]=data.get("Pasword",u["Pasword"])

            return {"Meassage": f" User {user_name} update sucsesfully "}
    return f" User not found "


#  Delete user

@app.delete("/users/<user_name>")
def delete_user(user_name):
    for u in users:
        if u["username"]==user_name:
            users.remove(u)

            return f"User {user_name} delete sucessfully"
        return f" User not found"

    
    
if __name__ == "__main__":
    app.run(debug=True)