참고자료: 클린코드를 위한 테스트 주도 개발
- - -

# 8장 스테이징 사이트를 이용한 배포 테스트
## 8.1 개요

1. 스테이징 서버에서 실행할 수 있도록 FT를 수정한다.   
2. 서버를 구축하고 거기에 필요한 모든 소프트웨어를 설치한다. 또한 스테이징과 운영 도메인이 이 서버를 가리키도록 설정한다.   
3. git을 이용해서 코드를 서버에 업로드한다.    
4. Django 개발 서버를 이용해서 스테이징 사이트에서 약식 버전의 사이트를 테스트 한다.   
5. Virtualenv 사용법을 배워서 서버에 있는 파이썬 의존 관계를 관리하도록 한다.   
6. 과정을 진행하면서 항시 FT를 실행한다. 이를 통해 단계별로 무엇이 동작하고, 무엇이 동작하지 않는지 확인한다.   
7. Gunicorn, Upstart, 도메인 소켓 등을 이용해서 사이트를 운영 서버에 배포하기 위한 설정을 한다.   
8. 설정이 정상적으로 동작하면 스크립트를 작성해서 수동으로 했던 작업을 자동화하도록 한다. 이를 통해 사이트 배포를 자동화할 수 있다.    
9. 마지막으로, 동일 스크립트를 이용해서 운영 버전의 사이트를 실제 도메인에 배포하도록한다.   



도메인: freenom .ga    
서버: digitalocean(Iaas 클라우드 컴퓨팅) 싱가포르    
os: ubuntu 18.04.5 LTS   
웹서버: nginx   
wsgi: gunicorn   
배포 자동화 도구: fabric   
웹 테스트 자동화 프레임워크: selenium   


/home/kjh   
├── sites   
│   ├── kjhwebsite-staging.ga    
│   │   ├── database   
│   │   ├── source    
│   │   ├── static    
│   │   └── virtualenv    
│   └── kjhwebsite.ga     
│       └── source...    

스테이징 사이트와 운영 사이트를 구분하고 다음과 같이 구축했습니다.

## 8.2 Nginx 설정 
웹 서버로 Nginx를 선택하였습니다.

    server {
       listen 80; @1
       server_name 139.59.238.46 kjhwebsite-staging.ga www.kjhwebsite-staging.ga; @2

       location /static { @3
            alias /home/kjh/sites/kjhwebsite-staging.ga/static;
       }

     location / {
                    proxy_set_header Host $host; @4
                    proxy_pass http://unix:/tmp/kjhwebsite-staging.ga.socket; @5
                }
    }

@1 80 포트로 http의 기본포트입니다.   
@2 책에서는 도메인만 적었지만 오류가 나서 IP, 도메인, www.도메인 세개다 적어놨습니다. 혹시 도메인만 적어놓고 오류가 난다면 세개다 적으시는걸 추천합니다.   
@3 정적파일들을 모아놓은 곳을 nginx에게 알려줍니다. runserver는 알아서 찾지만 웹서버는 모르기때문에 필요한 코드입니다.    
@4 client request의 header에 이 필드가 없으면 아무것도 전달되지 않습니다. 이러한 경우 $host 변수를 사용합니다.    
참고자료: http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header   
@5 유닉스 도메인 소켓으로 자세한 것은 8.4에서 설명합니다.

## 8.3 Gunicorn 

177p에는 upstart 이용한다고 나와있지만 책에 있는 코드를 작성하여 sudo start xxxxx를 실행하면 start 명령이 없다고 뜰겁니다.   
책이 2015쯤에 나왔기 때문에 2020년인 지금과 맞지 않습니다.   

/etc/systemd/system 디렉터리에 gunicorn.service 파일을 생성하여 아래와 같이 코드를 작성합니다.   


    [Unit]
    Description=gunicorn daemon
    After=network.target

    [Service]
    User=kjh
    Group=www-data
    WorkingDirectory=/home/kjh/sites/kjhwebsite-staging.ga/source
    ExecStart=/home/kjh/sites/kjhwebsite-staging.ga/virtualenv/bin/gunicorn \
            --bind unix:/tmp/kjhwebsite-staging.ga.socket \
             superlists.wsgi:application

    Restart=always

    [Install]
    WantedBy=multi-user.target


파일을 생성하고    
sudo systemctl start gunicorn    
sudo systemctl enable gunicorn    
으로 등록하면 됩니다. 오류가 난다면   
sudo systemctl status gunicorn으로 에러를 확인하세요.   

다 완료 했다면   
service gunicorn start로 키고   
service gunicorn stop으로 끄면 됩니다.   


## 8.4 유닉스 도메인 소켓(UDS)

유닉스 도메인 소켓(Unix Domain Socket)은 프로세스간의 데이터 교환을 위한 기술 중 하나로, 파일 시스템을 통해 소켓통신 방식으로 내부 프로세스간의 통신을 하는 구조로 이뤄져있습니다.  

message queue, shared memory와 같은 IPC(Inter Process Communication)의 일부입니다.   

UDS의 가장 큰 특징은 소켓통신 방식을 써서 만든 프로세스에 사용이 가능하기 때문에 소켓프로그래밍 구조를 유지한 채로 로컬 프로세스와의 효율적 통신을 가능케 한다는 점입니다. 

TCP, 혹은 UDP형식 데이터를 파일 시스템을 이용해서 통신하는 구조로, 파일 시스템을 통해 파일 주소 및 inode로 각 프로세스에서 참조되며,

통신은 운영체제의 커널상에서 이뤄지기 때문에 inet소켓을 이용해서 네트워크단을 이용해 전달하는 것보다 빠르며 부하가 적게 걸린다.

(기본적으로 소켓통신 방식이 TCP/IP의 4계층을 거쳐 전달되기 때문에 지연이 발생하는데   
반해서 유닉스 소켓은 어플리케이션 계층에서 TCP계층으로 내려가 바로 데이터를 전달하고, 수신측도 TCP계층에서 수신해 어플리케이션 계층으로 올라갑니다.)

# 9장 페브릭을 이용한 배포 자동화


    def _create_directory_structure_if_necessary(site_folder):
        for subfolder in ('database', 'static', 'virtualenv', 'source'):
            run('mkdir -p %s %s' % (site_folder, subfolder))

    def _get_latest_source(source_folder):
        if exists(source_folder + './git'):
            run('cd %s && git fetch' % (source_folder,))
        else:
            run('git clone %s %s' % (REPO_URL, source_folder))
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run('cd %s && git reset --hard %s' % (source_folder, current_commit))

    def _update_settings(source_folder, site_name):
        settings_path = source_folder + 'superlists/settings.py'
        sed(settings_path, "DEBUG = True", "DEBUG = False")
        sed(settings_path, 'ALLOWED_HOSTS =.+$', 'ALLOWED_HOSTS = ["%s"]' (site_name,))
        secret_key_file = source_folder + '/superlists/secret_key.py'
        if not exists(secret_key_file):
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
            append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
        append(settings_path, '\nfrom .secret_key import SECRET_KEY')

    def _update_virtualenv(source_folder):
        virtualenv_folder = source_folder + '/../virtualenv'
        if not exists(virtualenv_folder + '/bin/pip'):
            run('virtualenv -- python=python3 %s' % (virtual_folder,))
        run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))

    def _update_static_files(source_folder):
        run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' %(source_folder,))

    def _update_database(source_folder):
        run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder,))


# 10 입력 유효성 검사 및 테스트 구조화
## 10.1 테스트 구조화 197p ~ 206p
기능 테스트와 단위 테스트를 한 파일에 다 작성 하였는데 이러한 방법은 좋지 않습니다.    

기능 테스트를 한 폴더에 넣고 기능이나 사용자 스토리 단위로 테스트를 그룹화 합니다.    

이렇게 한 폴더에 넣을 떄 중요한 점은 __init__ 파일을 폴더에 넣어 줘야 패키지로 인식 된다는 점 입니다.    

반복되는 코드는 base 파일에 리팩터링합니다.   

    │  base.py   
    │  test_layout_and_styling.py    
    │  test_list_item_validation.py   
    │  test_simple_list_creation.py    
    │  __init__.py   

단위 테스트는 일반적으로 model, view, form로 나누어 별도 테스트 파일을 만듭니다.

이때 템플릿을 위한 단위테스트가 없는 이유는 '상수는 테스트 하지마라' 라는 큐칙 때문입니다.   

단위 테스트는 로직이나 흐름제어, 설정 등을 테스트합니다.

    │  test_forms.py    
    │  test_models.py    
    │  test_views.py    
    │  __init__.py   

## 10.2 뷰를 이용한 유효성 검사 207p~

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
           

이 단위 테스트를 실행하면 AssertError: ValidationError not raised 라는 결과가 나옵니다.     

TextField가 빈 값을 허용하지 않음에도 테스트가 실패하는 이유가 무엇일까요?

Django 모델은 저장 처리에 대해서 유효성 검사를 못하기 때문입니다. 데이터베이스 저장과 관련된 처리에선 에러가 발행하지만
SQLite의 경우 빈 값 제약을 강제적으로 부여할 수 없기 때문에 save 메소드가 빈 값을 그냥 통과시킵니다.     

이때 수동으로 유효성 검사를 하는 함수가 있는데 <a href="https://docs.djangoproject.com/en/3.1/ref/models/instances/#validating-objects">full_clean()</a>이라는 함수 입니다.   



# 11장 간단한 폼
Django의 폼은 다음과 같은 강력한 기능을 가지고 있습니다.
- 사용자 입력을 처리하고 검증해서 에러로 출력할 수 있다.
- HTML 입력 요소를 표시하기 위한 템플릿으로 사용할 수 있으며, 에러 메시지도 제공한다.
- 일부 폼은 데이터를 데이터 베이스에서 저장할 수도 있다.
## 11.1 일반 폼

일반 폼은 forms.Form 클래스를 상속받아 생성합니다.    

이 폼은 widget으로 하나하나 지정해야하여 조금 귀찮은 면이 있습니다.   

모델에 관련이 없을 때 쓰기 때문에 이 폼을 사용하진 않고 이해만 하고 넘어 갑니다.  


## 11.2 모델 폼

모델 폼은 forms.ModelForm 클래스를 상속받아 생성합니다.    
사용할 폼이 모델과 연관되어 있을 때 사용합니다.

모델에 정의한 필드만을 가지고 html 렌더링을 하기 때문에 이 폼을 사용하는 것이 훨씬 편리합니다.

Meta에선 폼이 어떤 모델을 이용할지와 어떤 필드를 사용할지를 정의합니다. 

뷰에서는 error를 정의하여 html에 렌더링하였지만 모델 폼에 error_messages를 정의하면 form 만 렌더링하면 form의 에러 메시지를 사용할 수 있습니다.

## 11.3 폼 자체 save 메소드 사용
save 메소드를 사용할때 아이템이 어떤 리스트에 소속되어지는지 알아야 합니다.

save 메소드에게 어떤 리스트에 저장해야 하는지 알려주면 코드를 줄일 수 있습니다.

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

# 12장 고급 폼




- - -
<h2>후기</h2>
