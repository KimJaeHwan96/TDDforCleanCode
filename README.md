<h2>참고자료: 클린코드를 위한 테스트 주도 개발 (초판: 2015)</h2>  
<img src="https://user-images.githubusercontent.com/64777061/95957617-e2268780-0e3a-11eb-8380-1d92c009541e.jpg" width="30%"></img>    
site: http://www.kjhwebsite-staging.ga/

- - -    
# 2장 unittest 모듈을 이용한 기능 테스트 확장
웹 애플리케이션을 실행하는 동안 로딩 시간을 고려해야합니다.     

코드가 아직로드되지 않은 요소에 액세스하려고하면 WebDriver에서 예외가 발생하고 스크립트가 중지됩니다.    
## 2.1 암시적 대기(implicit wait)
어떤 것을 검색할 때, 잠시 후에 검색결과가 나오는 것을 말합니다.     

네트워크 상황이나 기타 이유로 인하여 로딩에 시간이 걸릴 때 사용합니다.    

보통 get()을 사용하면 최대 3초까지 자동으로 대기하는데, 이 방법은 get()보다 더 오래 기다리게 할 수 있습니다.    

실행결과가 전부 로딩될 때 까지 기다린다고 생각하시면 될 것 같습니다.    

## 2.2 명시적 대기(explicit wait)
일부 요소가 로드되는 데 더 많은 시간이 소요될 때 암시적 대기는 브라우저가 모든 요소에 대해 동일한 시간 동안 불필요하게 대기하게 합니다.     

그런 면에서 명시적 대기는 특정 웹 요소에만 국한된 지능형 대기입니다.    

암시적인 대기를 해도 결과가 로드되지 않을 때에는, 셀레니움이 실행되면서 요소를 찾을 수가 없어 에러를 일으킬 수 있습니다.

이때에는 충분히 웹페이지의 찾고자하는 특정 요소가 로드된 후 실행될 수 있도록, 시간을 부여하여 명시적으로 대기할 수 있도록 해야합니다.    

## 2.3 유창한 대기(fluent wait)
암시적 및 명시적 대기와 달리 유창한 대기는 두 개의 매개 변수를 사용합니다.     

시간 종료 값 및 폴링 빈도. 시간 제한 값이 30 초이고 폴링 빈도가 2 초라고 가정 해 봅시다.    

WebDriver는 제한 시간 값 (30 초)까지 2 초마다 요소를 확인합니다. 결과없이 시간 초과 값이 초과되면 예외가 발생합니다.    


# 4장 왜 테스트를 하는 것인가?
## 4.1 TDD 프로세스
<img src="https://user-images.githubusercontent.com/64777061/96218675-36a73f80-0fc0-11eb-9314-8ada6e109e12.jpg" width="50%"></img>    


위 사진은 사용자입장에서 테스트하는 기능테스트와 개발자 입장에서 테스트하는 단위테스트 흐름도입니다. 기능테스트를 상위 테스트 관점으로 생각하면 됩니다.    

먼저 기능 테스트를 작성하고 실패하는지 확인합니다. "최소 코드 작성" 프로세스에선 작은 TDD 주기를 통해 테스트가 통과하도록 만듭니다.    
이때 하나 또는 그 이상의 단위 테스트를 작성하고 이를 단위 테스트-코드 주기에 넣어서 통과할 때까지 주기를 반복합니다.    
통과하면 다시 FT로 돌아가서 애플리케이션 코드를 수정합니다.(리팩터링) 수정 후에는 다시 단위 테스트를 실시해야합니다.    
기능 테스트 관점의 리팩터링은 어떻게 해야할까요? 이것은 애플리케이션 동작을 확인 하기 위해 기능 테스트를 사용하지만, 단위 테스트를 변경, 추가, 제거할 수 있음을 의미합니다.    

기능테스트는 애플리케이션이 동작하는지 판단하기 위한 궁극의 수단입니다. 반면 단위 테스트는 이판단을 돕기 위한 툴이라 할 수 있습니다.    

# 5장 사용자 입력 저장하기
## 5.1 csrf_token
65p 에서 home.html에 request를 보낸뒤 받은 reponse 내용과 render_to_string으로 받은 expected_html이 같은지 비교하는 코드가 있다

비교를 하면 assertEqual이 False를 assert하는데 print를 하여 내용을 보면 csrf_token 부분이 다르기 때문이다.

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)

이때는 이 메서드를 이용하여 각각에 넣어주면 해결이 된다.


## 5.2 레드, 그린, 리팩터 && 스트라이크 세 개면 리팩터
단위 테스트-코드 주기를 레드, 그린, 리팩터로 설명하는 경우도 있습니다.   

-실패할 단위 테스트를 작성함으로써 작업을 시작한다(레드).    

-이 테스트를 통과할 최소 코드를 작성한다(그린). 편법이라도 상관없다.    

-코드를 리팩터링해서 이해할 수 있는 코드로 만든다.    

리팩터링 단계에서 할 수 있는 한 가지 방법은 "중복을 제거"하는 것입니다.    

DRY(Don't Repeat Youerself)라는 원리가 있는데 스트라이크 세 개면 리팩터 이론과 일맥상통합니다.    

즉 한 번 정도는 복사-붙여넣기를 해줄 수 있지만, 같은 코드가 세번 등장하면 중복을 제거해야 하는 이론입니다.    

이때 두번이 아니라 세번인 이유는 더 일반화 할 수 있는 코드를 찾을 수 있기 때문입니다.     


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

deploy_tools/fabfile.py의 코드입니다

    def _create_directory_structure_if_necessary(site_folder):
        for subfolder in ('database', 'static', 'virtualenv', 'source'):
            run('mkdir -p %s %s' % (site_folder, subfolder)) @1 2
          
@1 run은 페브릭에서 가장 자주 사용되는 명령입니다. "이 셸 명령을 서버에서 실행해"라는 의미입니다.    

@2 mkdir -p는 상위 디렉터리도 작성해주며 이미 있는 폴더라도 에러가 발생하지 않습니다.    


    def _get_latest_source(source_folder):
        if exists(source_folder + './git'): @1
            run('cd %s && git fetch' % (source_folder,)) @2 3
        else:
            run('git clone %s %s' % (REPO_URL, source_folder)) @4
        current_commit = local("git log -n 1 --format=%H", capture=True) @5
        run('cd %s && git reset --hard %s' % (source_folder, current_commit)) @6


@1 서버에 파일 및 디렉터리가 존재하는지 확인합니다. .git이라는 숨겨진 폴더가 있는지 확인해서 리포지토리가 이미 폴더에 클론돼 있는지 확인하는 것입니다.    

@2 현재 디렉터리를 설정하기 위해서 많은 명령어가 cd로 시작합니다.     
패브릭은 상태 정보를 유지하지 않기 때문에, 어떤 디렉터리에서 명령이 실행됐는지 또 실행될것인지 기억하지 못합니다.      

@3 git fetch는 기존 리포지토리 폴더에 가장 최근에 커밋한 것을 웹으로부터 다운로드합니다.

@4 기존 리포지토리가 없으면 .git clone을 이용해서 지정한 리포지토리 URL로부터 폴더 구조를 포함한 전체 내용을 다운로드합니다.

@5 패브릭의 local 명령은 명령어를 로컬 장비에서 실행합니다. subprocess.Popen을 랩핑한 것으로 매우 편리합니다.     
여기서는 git log 출력 내용을 캡쳐해서 로컬 트리에 있는 현재 커밋해쉬를 취득합니다.     
이것은 로컬 장비에서 체크아웃한 상태와 동일한 상태로 서버가 종료된다는 것을 의미합니다.(단 서버에 push한 상태여야 합니다.)    

@6 reset --hard를 이용해서 서버의 코드 디렉터리에 발생한 모든 변경을 초기화합니다.    


    def _update_settings(source_folder, site_name):
        settings_path = source_folder + 'superlists/settings.py'
        sed(settings_path, "DEBUG = True", "DEBUG = False") @1
        sed(settings_path, 'ALLOWED_HOSTS =.+$', 'ALLOWED_HOSTS = ["%s"]' (site_name,)) 
        secret_key_file = source_folder + '/superlists/secret_key.py'
        if not exists(secret_key_file): @2
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
            append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
        append(settings_path, '\nfrom .secret_key import SECRET_KEY') @3 
        
@1 패브릭의 sed 명령은 파일 내에 있는 문자열을 특정 문자열로 변경합니다.     
@2 Django에선 암호화(쿠키과 CSRF 보호)를 위해서 SECRET_KEY를 이용합니다. 키를 이용할 때는 공개 중인 소스코드 리포지터리에 있는 비밀 키와 다른 키를 이용해야합니다.        
이 코드는 비밀 키가 존재하지 않으면 새로운 키를 만들어서 설정 파일에 임포트합니다.       
@3 append 명령은 파일 끝에 새로운 줄을 추가합니다. 이때 \n을 붙여주어야 문제가 생기지 않습니다.



    def _update_virtualenv(source_folder):
        virtualenv_folder = source_folder + '/../virtualenv'
        if not exists(virtualenv_folder + '/bin/pip'): 
            run('virtualenv -- python=python3 %s' % (virtual_folder,))
        run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder)) 


    def _update_static_files(source_folder):
        run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' %(source_folder,)) 

    def _update_database(source_folder):
        run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder,))

위에 세 개의 메소드들은 이름만으로 이해가 가기 때문에 크게 설명하지 않았습니다.    



아쉽게도 저는 패브릭을 완전히 이해하지 못했고 에러가 떠서 배포 자동화에 성공하지 못했습니다.      
뿐만아니라 인증을 위한 비밀번호를 요구하여 이또한 해결해야할 사항인 것 같습니다.
배포 자동화가 아주 간단한 것이 아니라는 것을 깨닫고 조금더 시간을 두어 고민해봐야할 문제인 것 같습니다. 

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

    class ExistingListItemForm(ItemForm):
            def __init__(self, for_list, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.instance.list = for_list

ItemForm을 상속받은 폼입니다. 기존 폼은 list를 계속 지정해줘야하는데 이 폼은 생성자에서 지정을 해주기 때문에 따로 list를 지정할 필요가 없습니다.   

            def validate_unique(self):
                try:
                    self.instance.validate_unique()
                except ValidationError as e:
                    e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
                    self._update_errors(e)

validate_unique 메소드는 필드의 uniqueness를 검증하는데 문제가 있으면 ValidationError를 raise합니다.    

그 후 검증 에러를 취해서 에러 메시지를 변경하고 다시 폼으로 전달합니다.    

        def save(self):
            return forms.models.ModelForm.save(self)
            
ItemForm은 list를 지정해줘야하기 때문에 인자에 for_list를 추가 했지만 이 폼은 이미 생성자에서 지정을 하였기 때문에 불필요합니다.

save 메소드를 오버라이드하는데 이때 super().save()를 하면 상속 받은 ItemForm의 save 메소드를 사용하므로 더 상위인 forms.models.ModelForm의 save 메소드를 사용합니다.    

- - -
<h2>후기</h2>
