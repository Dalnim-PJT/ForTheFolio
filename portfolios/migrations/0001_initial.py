# Generated by Django 3.2.18 on 2023-08-07 03:16


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import portfolios.models
from portfolios.models import TechStack as Tech

def insert_techstack_data(apps, schema_editor):
    TechStack = apps.get_model('portfolios', 'TechStack')
    STACK_CHOICES = Tech.STACK_CHOICES
    for i, choice in enumerate(STACK_CHOICES, start=1):
        TechStack.objects.create(pk=i, stack=choice[0])

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mydatas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=portfolios.models.Mydatas.Mydatas_profileimage_path)),
                ('job', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('introduction', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='P_templates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('like_users', models.ManyToManyField(blank=True, null=True, related_name='like_templates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TechStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack', models.CharField(choices=[('Agit', 'Agit'), ('Airflow', 'Airflow'), ('Alamofire', 'Alamofire'), ('Android', 'Android'), ('Angular', 'Angular'), ('Ansible', 'Ansible'), ('Apollo', 'Apollo'), ('Appium', 'Appium'), ('ArangoDB', 'ArangoDB'), ('Arcus', 'Arcus'), ('ArgoCD', 'ArgoCD'), ('Armeria', 'Armeria'), ('Asana', 'Asana'), ('ASP.NET', 'ASP.NET'), ('AWS Athena', 'AWS Athena'), ('AWS AuroraDB', 'AWS AuroraDB'), ('AWS CodeBuild', 'AWS CodeBuild'), ('AWS CodeDeploy', 'AWS CodeDeploy'), ('AWS CodePipeline', 'AWS CodePipeline'), ('AWS DocumentDB', 'AWS DocumentDB'), ('AWS DynamoDB', 'AWS DynamoDB'), ('AWS Kinesis', 'AWS Kinesis'), ('AWS MariaDB', 'AWS MariaDB'), ('AWS Redshift', 'AWS Redshift'), ('AWS SES', 'AWS SES'), ('AWS SNS', 'AWS SNS'), ('AWS SQS', 'AWS SQS'), ('Azure DevOps', 'Azure DevOps'), ('Backb oneJS', 'BackboneJS'), ('Bazel', 'Bazel'), ('Bitbucket', 'Bitbucket'), ('Bitrise', 'Bitrise'), ('C#', 'C#'), ('C++', 'C++'), ('Capostrano', 'Capostrano'), ('CassandraDB', 'CassandraDB'), ('Celery', 'Celery'), ('CentOS', 'CentOS'), ('Central Dogma', 'Central Dogma'), ('Ceph', 'Ceph'), ('Cicle CI', 'Cicle CI'), ('Clickhouse', 'Clickhouse'), ('Clojure', 'Clojure'), ('CockroachDB', 'CockroachDB'), ('Codelgniter', 'Codelgniter'), ('Confluence', 'Confluence'), ('Couchbase', 'Couchbase'), ('CSS', 'CSS'), ('Cubrid', 'Cubrid'), ('Cucumber', 'Cucumber'), ('Cypress', 'Cypress'), ('Dagger', 'Dagger'), ('Dart', 'Dart'), ('Discord', 'Discord'), ('Django', 'Django'), ('Docker', 'Docker'), ('Docusaurus', 'Docusaurus'), ('Dooray', 'Dooray'), ('Drone', 'Drone'), ('Dropwizard', 'Dropwizard'), ('Druid', 'Druid'), ('ElasticSearch', 'ElasticSearch'), ('Electron', 'Electron'), ('Elixir', 'Elixir'), ('EmberJS', 'EmberJS'), ('Emotion', 'Emotion'), ('Envoy', 'Envoy'), ('Enzyme', 'Enzyme'), ('ExoPlayer', 'ExoPlayer'), ('ExpressJS', 'ExpressJS'), ('Falcon', 'Falcon'), ('FastAPI', 'FastAPI'), ('Fastify', 'Fastify'), ('Fastlane', 'Fastlane'), ('Fiber', 'Fiber'), ('Flask', 'Flask'), ('Flink', 'Flink'), ('Flow', 'Flow'), ('Fluentd', 'Fluentd'), ('Flutter', 'Flutter'), ('FreeBSD', 'FreeBSD'), ('Gatsby', 'Gatsby'), ('Gin', 'Gin'), ('Github', 'Github'), ('Github Action', 'Github Action'), ('Gitlab', 'Gitlab'), ('Glide', 'Glide'), ('Go', 'Go'), ('Go CD', 'Go CD'), ('Google BigQuery', 'Google BigQuery'), ('Google Cloud Build', 'Google Cloud Build'), ('Google Data Studio', 'Google Data Studio'), ('Google Firebase', 'Google Firebase'), ('Google Firestore', 'Google Firestore'), ('Grafana', 'Grafana'), ('GraphQL', 'GraphQL'), ('Greenplum', 'Greenplum'), ('GRPC', 'GRPC'), ('Gulp', 'Gulp'), ('H2', 'H2'), ('Hadoop', 'Hadoop'), ('Harbor', 'Harbor'), ('Hazelcast', 'Hazelcast'), ('Hbase', 'Hbase'), ('Helm', 'Helm'), ('Hibernate', 'Hibernate'), ('Hive', 'Hive'), ('HTML', 'HTML'), ('Hugo', 'Hugo'), ('Immer', 'Immer'), ('Impala', 'Impala'), ('InfluxDB', 'InfluxDB'), ('iOS', 'iOS'), ('Istio', 'Istio'), ('Jaeger', 'Jaeger'), ('Jandi', 'Jandi'), ('Jasmine', 'Jasmine'), ('Java', 'Java'), ('JavaScript', 'JavaScript'), ('Jenkins', 'Jenkins'), ('Jest', 'Jest'), ('Jira', 'Jira'), ('Jotai', 'Jotai'), ('JUnit', 'JUnit'), ('Kafka', 'Kafka'), ('KakaoWork', 'KakaoWork'), ('Kakotalk', 'Kakotalk'), ('Karma', 'Karma'), ('Karpenter', 'Karpenter'), ('Keras', 'Keras'), ('Kibana', 'Kibana'), ('Koa', 'Koa'), ('Kotlin', 'Kotlin'), ('Ktor', 'Ktor'), ('Kube-Bench', 'Kube-Bench'), ('Kubeflow', 'Kubeflow'), ('Kubernetes', 'Kubernetes'), ('Kudu', 'Kudu'), ('Laravel', 'Laravel'), ('Linkerd', 'Linkerd'), ('Linux', 'Linux'), ('Liquibase', 'Liquibase'), ('Locust', 'Locust'), ('Looker', 'Looker'), ('Lottie', 'Lottie'), ('Lua', 'Lua'), ('Luigi', 'Luigi'), ('macOS', 'macOS'), ('Memcached', 'Memcached'), ('Metabase', 'Metabase'), ('Meteor', 'Meteor'), ('Microsoft-Teams', 'Microsoft-Teams'), ('MLflow', 'MLflow'), ('MobX', 'MobX'), ('Mocha', 'Mocha'), ('Mockito', 'Mockito'), ('Monday', 'Monday'), ('MongoDB', 'MongoDB'), ('Moya', 'Moya'), ('MSSQL', 'MSSQL'), ('MyBatis', 'MyBatis'), ('MySQL', 'MySQL'), ('Naver Works', 'Naver Works'), ('Neo4j', 'Neo4j'), ('NestJS', 'NestJS'), ('Netty', 'Netty'), ('NextJS', 'NextJS'), ('Nexus', 'Nexus'), ('nGrinder', 'nGrinder'), ('NIFI', 'NIFI'), ('NodeJS', 'NodeJS'), ('Notion', 'Notion'), ('NuxtJS', 'NuxtJS'), ('Objective-C', 'Objective-C'), ('OpenEBS', 'OpenEBS'), ('OpenGL', 'OpenGL'), ('OracleDB', 'OracleDB'), ('Packer', 'Packer'), ('Perl', 'Perl'), ('Phoenix', 'Phoenix'), ('PHP', 'PHP'), ('Playwright', 'Playwright'), ('PostgreSQL', 'PostgreSQL'), ('Presto', 'Presto'), ('Prometheus', 'Prometheus'), ('Puppeteer', 'Puppeteer'), ('Python', 'Python'), ('Pytorch', 'Pytorch'), ('R', 'R'), ('RabbitMQ', 'RabbitMQ'), ('Rancher', 'Rancher'), ('Ranger', 'Ranger'), ('Ray', 'Ray'), ('React Context', 'React Context'), ('React Native', 'React Native'), ('React Query', 'React Query'), ('ReactiveX', 'ReactiveX'), ('ReactJS', 'ReactJS'), ('ReactorKit', 'ReactorKit'), ('Realm', 'Realm'), ('Realy', 'Realy'), ('Recoil', 'Recoil'), ('Redash', 'Redash'), ('Redis', 'Redis'), ('Redux', 'Redux'), ('ReScript', 'ReScript'), ('Rest-Assured', 'Rest-Assured'), ('Retrofit', 'Retrofit'), ('RIBs', 'RIBs'), ('RocksDB', 'RocksDB'), ('Ruby', 'Ruby'), ('Ruby on Rails', 'Ruby on Rails'), ('Rundeck', 'Rundeck'), ('Rust', 'Rust'), ('Saltstack', 'Saltstack'), ('Sanic', 'Sanic'), ('Scala', 'Scala'), ('Selenium', 'Selenium'), ('Sinon', 'Sinon'), ('Slack', 'Slack'), ('SnapKit', 'SnapKit'), ('Snowflake', 'Snowflake'), ('Solaris', 'Solaris'), ('Solr', 'Solr'), ('Sonarqube', 'Sonarqube'), ('Spark', 'Spark'), ('Spinnaker', 'Spinnaker'), ('Spring', 'Spring'), ('SpringBoot', 'SpringBoot'), ('Storybook', 'Storybook'), ('Styled-Components', 'Styled-Components'), ('Superest', 'Superest'), ('Svelte', 'Svelte'), ('Swagger', 'Swagger'), ('Swift', 'Swift'), ('Tableau', 'Tableau'), ('Telegram', 'Telegram'), ('Tensorflow', 'Tensorflow'), ('Terraform', 'Terraform'), ('Testing Library', 'Testing Library'), ('Thrift', 'Thrift'), ('Tilwind', 'Tilwind'), ('Traefik', 'Traefik'), ('Travis CI', 'Travis CI'), ('Trello', 'Trello'), ('Trino', 'Trino'), ('Tuist', 'Tuist'), ('TypeScript', 'TypeScript'), ('Ubuntu', 'Ubuntu'), ('Unity', 'Unity'), ('Unix', 'Unix'), ('Vault', 'Vault'), ('Visual Studio', 'Visual Studio'), ('Visual Studio Code', 'Visual Studio Code'), ('VueJS', 'VueJS'), ('Vuex', 'Vuex'), ('WebRTC', 'WebRTC'), ('Windows', 'Windows'), ('Zabbix', 'Zabbix'), ('Zeppelin', 'Zeppelin'), ('Zipkin', 'Zipkin'), ('Zustand', 'Zustand')], max_length=40)),
            ],
        ),
        migrations.RunPython(insert_techstack_data),
        migrations.CreateModel(
            name='Portfolios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=portfolios.models.Portfolios.Portfolio_profileimage_path)),
                ('job', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('introduction', models.TextField()),
                ('stack', models.ManyToManyField(related_name='portfolio_stacks', to='portfolios.TechStack')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolios.p_templates')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pjts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('pjts_content', models.TextField()),
                ('role', models.TextField()),
                ('github', models.URLField(blank=True, null=True)),
                ('web', models.URLField(blank=True, null=True)),
                ('mydata', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.mydatas')),
                ('portfolio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.portfolios')),
                ('stack', models.ManyToManyField(related_name='pjt_stacks', to='portfolios.TechStack')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pjtimages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=portfolios.models.Pjtimages.Pjt_image_path)),
                ('mydata', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.mydatas')),
                ('pjt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolios.pjts')),
                ('portfolio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.portfolios')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='P_exampleuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('job', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('introduction', models.TextField()),
                ('stack', models.ManyToManyField(related_name='template_stacks', to='portfolios.TechStack')),
            ],
        ),
        migrations.AddField(
            model_name='mydatas',
            name='stack',
            field=models.ManyToManyField(related_name='mydata_stacks', to='portfolios.TechStack'),
        ),
        migrations.AddField(
            model_name='mydatas',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(choices=[('GitHub', 'GitHub'), ('Youtube', 'Youtube'), ('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('Notion', 'Notion'), ('Link', 'Link'), ('Google Drive', 'Google Drive'), ('LinkedIn', 'LinkedIn'), ('Blog', 'Blog'), ('Behance', 'Behance'), ('Brunch', 'Brunch'), ('Medium', 'Medium')], max_length=20)),
                ('link_content', models.URLField()),
                ('mydata', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.mydatas')),
                ('portfolio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.portfolios')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('career_content', models.TextField()),
                ('mydata', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.mydatas')),
                ('portfolio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolios.portfolios')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]