from fastapi import APIRouter, Request, Cookie, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, func
from sqlalchemy.exc import SQLAlchemyError
from typing import Union
from models import session
from models import session
from models.user import User
from models.estate import Estate
from models.favourite import Favourite
from models.estates_ind import EstatesInd


api_routes = APIRouter(prefix="/api")

templates = Jinja2Templates(directory="templates")


@api_routes.post("/users")
def create_user(name: str, email: str, password: str):
    # cria o usuário na memória
    user = User(name=name, email=email, password=password)
    # adiciona ele no banco de dados
    session.add(user)
    try:
        # salva as alterações
        session.commit()
        # resposta com os dados do usuário
        return JSONResponse(content=user.to_view(), status_code=201)
    # se o usuário for inválido
    except SQLAlchemyError:
        # remover aletarções
        session.rollback()
        # resposta de erro
        return JSONResponse({"message": "INVALID DATA"}, status_code=400)


# LOGIN DE USUÁRIO
@api_routes.post("/users/login")
def login_user(email: str, password: str):
    # query para ver se o usuário existe
    user = session.query(User).filter_by(email=email).first()
    # checa se a senha está correta
    if not user or user.password != password:
        # se não, erro de acesso proibido
        return JSONResponse({"message": "INVALID PASSWORD OR EMAIL"}, status_code=403)

    # se está tudo bem, mostrar o usuário e salvar o cookie
    resp = JSONResponse(content=user.to_view(), status_code=201)
    resp.set_cookie(key="login", value=user.id)
    return resp


# TESTE DE ACESSO PROTEGIDO
# @api_routes.get("/protected")
# def restricted(login: Union[str, None] = Cookie(default=None)):
#     user = session.query(User).filter_by(id=login).first()
#     if user:
#         return JSONResponse({"message": f"WELCOME {user.name}"})
#     else:
#         return JSONResponse({"message": "ACCESS FORBIDEN"}, 403)


# listagem de imóveis
@api_routes.get("/estates")
def list_estates(login: Union[str, None] = Cookie(default=None)):
    # Validar se o usuário está logado
    user = session.query(User).filter_by(id=login).first()
    if not user:
        return JSONResponse({"message": "ACCESS FORBIDEN"}, 403)

    # subquery para pegar a leitura mais recente dos imóveis
    subquery = (
        session.query(Estate.source_id, func.max(Estate.timestamp).label("timestamp"))
        .group_by(Estate.source_id)
        .subquery()
    )

    # query para pegar os imóveis da subquery
    estates = (
        session.query(Estate)
        .join(
            subquery,
            and_(
                subquery.c.source_id == Estate.source_id,
                subquery.c.timestamp == Estate.timestamp,
            ),
        )
        .all()
    )

    # responder os imóveis listados
    return JSONResponse(list(map(lambda e: e.to_view(), estates)))


@api_routes.post("/favourite")
def favourite_estate(
    estate_source_id: str,
    favourite: bool,
    login: Union[str, None] = Cookie(default=None),
):
    # Validar se o usuário está logado
    user = session.query(User).filter_by(id=login).first()
    if not user:
        return JSONResponse({"message": "ACCESS FORBIDEN"}, 403)

    favourite = Favourite(
        user_id=user.id,
        estate_ind_source_id=estate_source_id,
        favourited=1 if favourite else 0,
    )
    session.add(favourite)
    try:
        # salva as alterações
        session.commit()
        # resposta com os dados do favorito
        return JSONResponse(content=favourite.to_view(), status_code=201)
    # se o favorito for inválido
    except SQLAlchemyError:
        # remover aletarções
        session.rollback()
        # resposta de erro
        return JSONResponse({"message": "INVALID DATA"}, status_code=400)


# ========= HTML CONTROLLER =========
@api_routes.get("/login", response_class=HTMLResponse)
def login_page(req: Request):
    return templates.TemplateResponse("login.html", {"request": req, "title": "LOGIN"})


@api_routes.post("/validate", response_class=HTMLResponse)
def validate_page(req: Request, email: str = Form(), password: str = Form()):
    user = session.query(User).filter_by(email=email).first()
    if not user or user.password != password:
        return RedirectResponse("/login")

    resp = RedirectResponse("/estates", 303)
    resp.set_cookie(key="login", value=user.id)
    return resp


@api_routes.get("/estates", response_class=HTMLResponse)
def protected_page(req: Request, login: Union[str, None] = Cookie(default=None)):
    user = session.query(User).filter_by(id=login).first()
    if not user:
        return RedirectResponse("/login")

    estates = session.query(Estate).all()

    return templates.TemplateResponse(
        "estates.html",
        {
            "request": req,
            "title": "PROTECTED",
            "user": user.to_view(),
            "estates": estates,
        },
    )
