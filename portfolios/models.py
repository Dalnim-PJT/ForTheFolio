from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class TechStack(models.Model):
    STACK_CHOICES = [("Agit", "Agit"),("Airflow", "Airflow"),("Alamofire", "Alamofire"),("Android", "Android"),("Angular", "Angular"),
                    ("Ansible", "Ansible"),("Apollo", "Apollo"),("Appium", "Appium"),("ArangoDB", "ArangoDB"),("Arcus", "Arcus"),("ArgoCD", "ArgoCD"),
                    ("Armeria", "Armeria"),("Asana", "Asana"),("ASP.NET", "ASP.NET"),("AWS Athena", "AWS Athena"),("AWS AuroraDB", "AWS AuroraDB"),
                    ("AWS CodeBuild", "AWS CodeBuild"),("AWS CodeDeploy", "AWS CodeDeploy"),("AWS CodePipeline", "AWS CodePipeline"),
                    ("AWS DocumentDB", "AWS DocumentDB"),("AWS DynamoDB", "AWS DynamoDB"),("AWS Kinesis", "AWS Kinesis"),("AWS MariaDB", "AWS MariaDB"),
                    ("AWS Redshift", "AWS Redshift"),("AWS SES", "AWS SES"),("AWS SNS", "AWS SNS"),("AWS SQS", "AWS SQS"),
                    ("Azure DevOps", "Azure DevOps"),("Backb oneJS", "BackboneJS"),("Bazel", "Bazel"),("Bitbucket", "Bitbucket"),("Bitrise", "Bitrise"),
                    ("C#", "C#"),("C++", "C++"),("Capostrano", "Capostrano"),("CassandraDB", "CassandraDB"),("Celery", "Celery"),("CentOS", "CentOS"),
                    ("Central Dogma", "Central Dogma"),("Ceph", "Ceph"),("Cicle CI", "Cicle CI"),("Clickhouse", "Clickhouse"),("Clojure", "Clojure"),
                    ("CockroachDB", "CockroachDB"),("Codelgniter", "Codelgniter"),("Confluence", "Confluence"),("Couchbase", "Couchbase"),
                    ("Cubrid", "Cubrid"),("Cucumber", "Cucumber"),("Cypress", "Cypress"),("Dagger", "Dagger"),("Dart", "Dart"),("Discord", "Discord"),
                    ("Django", "Django"),("Docker", "Docker"),("Docusaurus", "Docusaurus"),("Dooray", "Dooray"),("Drone", "Drone"),
                    ("Dropwizard", "Dropwizard"),("Druid", "Druid"),("ElasticSearch", "ElasticSearch"),("Electron", "Electron"),("Elixir", "Elixir"),
                    ("EmberJS", "EmberJS"),("Emotion", "Emotion"),("Envoy", "Envoy"),("Enzyme", "Enzyme"),("ExoPlayer", "ExoPlayer"),
                    ("ExpressJS", "ExpressJS"),("Falcon", "Falcon"),("FastAPI", "FastAPI"),("Fastify", "Fastify"),("Fastlane", "Fastlane"),
                    ("Fiber", "Fiber"),("Flask", "Flask"),("Flink", "Flink"),("Flow", "Flow"),("Fluentd", "Fluentd"),("Flutter", "Flutter"),
                    ("FreeBSD", "FreeBSD"),("Gatsby", "Gatsby"),("Gin", "Gin"),("Github", "Github"),("Github Action", "Github Action"),
                    ("Gitlab", "Gitlab"),("Glide", "Glide"),("Go", "Go"),("Go CD", "Go CD"),("Google BigQuery", "Google BigQuery"),
                    ("Google Cloud Build", "Google Cloud Build"),("Google Data Studio", "Google Data Studio"),("Google Firebase", "Google Firebase"),
                    ("Google Firestore", "Google Firestore"),("Grafana", "Grafana"),("GraphQL", "GraphQL"),("Greenplum", "Greenplum"),("GRPC", "GRPC"),
                    ("Gulp", "Gulp"),("H2", "H2"),("Hadoop", "Hadoop"),("Harbor", "Harbor"),("Hazelcast", "Hazelcast"),("Hbase", "Hbase"),
                    ("Helm", "Helm"),("Hibernate", "Hibernate"),("Hive", "Hive"),("Hugo", "Hugo"),("Immer", "Immer"),("Impala", "Impala"),
                    ("InfluxDB", "InfluxDB"),("iOS", "iOS"),("Istio", "Istio"),("Jaeger", "Jaeger"),("Jandi", "Jandi"),("Jasmine", "Jasmine"),
                    ("Java", "Java"),("JavaScript", "JavaScript"),("Jenkins", "Jenkins"),("Jest", "Jest"),("Jira", "Jira"),("Jotai", "Jotai"),
                    ("JUnit", "JUnit"),("Kafka", "Kafka"),("KakaoWork", "KakaoWork"),("Kakotalk", "Kakotalk"),("Karma", "Karma"),
                    ("Karpenter", "Karpenter"),("Keras", "Keras"),("Kibana", "Kibana"),("Koa", "Koa"),("Kotlin", "Kotlin"),("Ktor", "Ktor"),
                    ("Kube-Bench", "Kube-Bench"),("Kubeflow", "Kubeflow"),("Kubernetes", "Kubernetes"),("Kudu", "Kudu"),("Laravel", "Laravel"),
                    ("Linkerd", "Linkerd"),("Linux", "Linux"),("Liquibase", "Liquibase"),("Locust", "Locust"),("Looker", "Looker"),("Lottie", "Lottie"),
                    ("Lua", "Lua"),("Luigi", "Luigi"),("macOS", "macOS"),("Memcached", "Memcached"),("Metabase", "Metabase"),("Meteor", "Meteor"),
                    ("Microsoft-Teams", "Microsoft-Teams"),("MLflow", "MLflow"),("MobX", "MobX"),("Mocha", "Mocha"),("Mockito", "Mockito"),
                    ("Monday", "Monday"),("MongoDB", "MongoDB"),("Moya", "Moya"),("MSSQL", "MSSQL"),("MyBatis", "MyBatis"),("MySQL", "MySQL"),
                    ("Naver Works", "Naver Works"),("Neo4j", "Neo4j"),("NestJS", "NestJS"),("Netty", "Netty"),("NextJS", "NextJS"),("Nexus", "Nexus"),
                    ("nGrinder", "nGrinder"),("NIFI", "NIFI"),("NodeJS", "NodeJS"),("Notion", "Notion"),("NuxtJS", "NuxtJS"),
                    ("Objective-C", "Objective-C"),("OpenEBS", "OpenEBS"),("OpenGL", "OpenGL"),("OracleDB", "OracleDB"),("Packer", "Packer"),
                    ("Perl", "Perl"),("Phoenix", "Phoenix"),("PHP", "PHP"),("Playwright", "Playwright"),("PostgreSQL", "PostgreSQL"),
                    ("Presto", "Presto"),("Prometheus", "Prometheus"),("Puppeteer", "Puppeteer"),("Python", "Python"),("Pytorch", "Pytorch"),("R", "R"),
                    ("RabbitMQ", "RabbitMQ"),("Rancher", "Rancher"),("Ranger", "Ranger"),("Ray", "Ray"),("React Context", "React Context"),
                    ("React Native", "React Native"),("React Query", "React Query"),("ReactiveX", "ReactiveX"),("ReactJS", "ReactJS"),
                    ("ReactorKit", "ReactorKit"),("Realm", "Realm"),("Realy", "Realy"),("Recoil", "Recoil"),("Redash", "Redash"),("Redis", "Redis"),
                    ("Redux", "Redux"),("ReScript", "ReScript"),("Rest-Assured", "Rest-Assured"),("Retrofit", "Retrofit"),("RIBs", "RIBs"),
                    ("RocksDB", "RocksDB"),("Ruby", "Ruby"),("Ruby on Rails", "Ruby on Rails"),("Rundeck", "Rundeck"),("Rust", "Rust"),
                    ("Saltstack", "Saltstack"),("Sanic", "Sanic"),("Scala", "Scala"),("Selenium", "Selenium"),("Sinon", "Sinon"),("Slack", "Slack"),
                    ("SnapKit", "SnapKit"),("Snowflake", "Snowflake"),("Solaris", "Solaris"),("Solr", "Solr"),("Sonarqube", "Sonarqube"),
                    ("Spark", "Spark"),("Spinnaker", "Spinnaker"),("Spring", "Spring"),("SpringBoot", "SpringBoot"),("Storybook", "Storybook"),
                    ("Styled-Components", "Styled-Components"),("Superest", "Superest"),("Svelte", "Svelte"),("Swagger", "Swagger"),
                    ("Swift", "Swift"),("Tableau", "Tableau"),("Telegram", "Telegram"),("Tensorflow", "Tensorflow"),("Terraform", "Terraform"),
                    ("Testing Library", "Testing Library"),("Thrift", "Thrift"),("Tilwind", "Tilwind"),("Traefik", "Traefik"),("Travis CI", "Travis CI"),
                    ("Trello", "Trello"),("Trino", "Trino"),("Tuist", "Tuist"),("TypeScript", "TypeScript"),("Ubuntu", "Ubuntu"),("Unity", "Unity"),
                    ("Unix", "Unix"),("Vault", "Vault"),("VueJS", "VueJS"),("Vuex", "Vuex"),("WebRTC", "WebRTC"),("Windows", "Windows"),
                    ("Zabbix", "Zabbix"),("Zeppelin", "Zeppelin"),("Zipkin", "Zipkin"),("Zustand", "Zustand")
                    ]
    stack = models.CharField(max_length=20, choices=STACK_CHOICES)


# 제공하는 템플릿 모델
class P_templates(models.Model):
    title = models.CharField(max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_templates')

    def __str__(self):
        return self.title


# 제공하는 템플릿 모델에 사용되는 예시 유저 정보
class P_exampleuser(models.Model):
    username = models.CharField(max_length=50)
    job = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    introduction = models.TextField()
    stack = models.ManyToManyField(TechStack, related_name="template_stacks")


# 사용자의 정보를 입력해놓는 모델
class Mydatas(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def Mydatas_profileimage_path(instance, filename):
        return f'Mydatas/profile/{instance.user.email}/{filename}'
    image = ProcessedImageField(upload_to=Mydatas_profileimage_path, blank=True, null=True, processors=[ResizeToFill(100,100)])
    job = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    introduction = models.TextField()
    stack = models.ManyToManyField(TechStack, related_name="mydata_stacks")


# 포트폴리오에 저장하는 모델
class Portfolios(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(P_templates, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

    def Portfolio_profileimage_path(instance, filename):
        return f'Portfolio/profile/{instance.user.email}/{filename}'
    image = ProcessedImageField(upload_to=Portfolio_profileimage_path, blank=True, null=True, processors=[ResizeToFill(100,100)])
    job = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    introduction = models.TextField()
    stack = models.ManyToManyField(TechStack, related_name="portfolio_stacks")


# 중복을 피하기 위한 가상 모델
class BaseInfo(models.Model):
    mydata = models.ForeignKey(Mydatas, on_delete=models.CASCADE, null=True, blank=True)
    portfolio = models.ForeignKey(Portfolios, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True


class Links(BaseInfo):
    LINK_CHOICES = [('GitHub', 'GitHub'), ('Youtube','Youtube'), ('Facebook','Facebook'), ('Instagram', 'Instagram'),
                    ('Notion', 'Notion'), ('Link', 'Link'), ('Google Drive', 'Google Drive'), ('LinkedIn', 'LinkedIn'), ('Blog', 'Blog'),
                    ('Behance', 'Behance'), ('Brunch', 'Brunch'), ('Medium', 'Medium'),]
    link = models.CharField(max_length=20, choices=LINK_CHOICES)
    link_content = models.URLField()


class Career(BaseInfo):
    career_content = models.TextField()


class Pjts(BaseInfo):
    name = models.CharField(max_length=50)
    pjts_content = models.TextField()
    role = models.TextField()
    stack = models.ManyToManyField(TechStack, related_name="pjt_stacks")


class Pjtimages(BaseInfo):
    pjt = models.ForeignKey(Pjts, on_delete=models.CASCADE)
    def Pjt_image_path(instance, filename):
        return f'pjt/{instance.pjt.mydata.user.pk}/{instance.pjt.mydata.title}/{filename}'
    image = ProcessedImageField(upload_to=Pjt_image_path, blank=True, null=True)
    