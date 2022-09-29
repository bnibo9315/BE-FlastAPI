from pydoc import text
from fastapi import FastAPI, HTTPException, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
    get_redoc_html,
)
title = 'FastAPI - Backend Dev'
version = '0.1.1'
docs_url = '/documents'
redoc_url = '/docsV2'

description = """
<details  close><summary>About me</summary>
<div id="header" align="center">
  <img src="https://raw.githubusercontent.com/qlongdevdn/qlongdevdn/main/assets/logo_header.gif" style="width:700px;"/>
  <a href="https://www.facebook.com/quanglongdev.dn/"></a>
</div>



<div id="badges"  align="center">
  <a href="https://www.facebook.com/quanglongdev.dn/">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Badge"/>
  </a>
  <a href="https://www.instagram.com/qlongdev/">
    <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram Badge"/>
  </a>
  <a href="https://gitlab.com/quanglongdevDN">
    <img src="https://img.shields.io/badge/GitLab-330F63?style=for-the-badge&logo=gitlab&logoColor=white" alt="GitLab Badge"/>
  </a>
  <a href="https://www.facebook.com/quanglongdev.dn">
    <img src="https://img.shields.io/badge/SoundCloud-FF3300?style=for-the-badge&logo=soundcloud&logoColor=white" alt="SoundCloud Badge"/>
  </a>
</div>




# Hi there 👋 I'm Quang Long - Developer in Da Nang City, Viet Nam

<br></br>


- 🔭 I’m currently working on Hekate Artificial Intelligence company

- 🌱 I’m AI Developer and Backend Developer ( sometime Fullstack Developer 😚😚😚😚😚 ) 

- 👯 I have strengths in Python and PHP languages

- 👺 Some projects have been implemented such as Medical Project - using Ai detect the thrombosis in the brain

- 📩 Ask me about at gmail : quanglong.devdn@gmail.com


<br></br>


<div align=center>

  ![GitHub Streak](http://github-readme-streak-stats.herokuapp.com?user=qlongdevdn&theme=dark&hide_border=true&fire=DD2727)

</div>
<br></br>

<div align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/anaconda/anaconda-original.svg" title="Anaconda" alt="Anaconda" width="40" height="40"/>&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-plain-wordmark.svg"  title="CSS3" alt="CSS" width="40" height="40"/>&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" title="JavaScript" alt="JavaScript" width="40" height="40"/>&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" title="MySQL"  alt="MySQL" width="40" height="40"/>&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original-wordmark.svg" title="NodeJS" alt="NodeJS" width="40" height="40"/>&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" title="AWS" alt="AWS" width="40" height="40"/>&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original-wordmark.svg" title="Git" **alt="Git" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/apache/apache-original.svg" title="Apache" **alt="Apache" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" title="Python" **alt="Python" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/cakephp/cakephp-original.svg" title="cakephp" **alt="cakephp" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/php/php-original.svg" title="php" **alt="php" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/ssh/ssh-original-wordmark.svg" title="ssh" **alt="ssh" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/c/c-original.svg" title="C" **alt="C" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg" title="fastapi" **alt="fastapi" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/flask/flask-original.svg" title="flask" **alt="flask" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original-wordmark.svg" title="Git" **alt="Git" width="40" height="40"/>
</div>

</details>

"""

app = FastAPI(title=title, version=version, docs_url=None,
              description=description, redoc_url=None,)


responsesDetail = {
    405: {
        'status': False,
        'message': "Method not allowed. Please try with another method or read the documentation api"
    }
}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 405:
        response = JSONResponse({
            'status': False,
            'message': "Method not allowed. Please try with another method or read the documentation api",
            'code': 405
        })
    else:
        response = JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder({
                'status': False,
                'message': str(exc.detail) + ". Please read the documentation api",
                'code': exc.status_code
            }))
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"status": False,
                                  "message": "Action false. Check data form ",
                                  "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                                  "detail": exc.errors()}),
    )


@app.get("/documents", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.14.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.14.0/swagger-ui.css")


@app.get("/docsV2", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title,
        redoc_js_url="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js",
    )
