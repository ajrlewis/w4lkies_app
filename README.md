# w4lkies_app

![My Package Logo](static/img/logo.png)

## About

Public repository for the https://w4lkies.com website - a server-side rendered web application optimized for deployment using a web hosting service provided by Gandi. This repository contains HTML/CSS templates that are served with Python/Flask modules.

## Downloading & Installing

Clone the publicly available project as follows:

```bash
git clone https://github.com/ajrlewis/w4lkies_app.git
cd w4lkies_app
```

Install the dependencies and create the initial database migration using following scripts:

```bash
bash scripts/install.sh
bash scripts/migrate.sh init
```

These scripts should create a virtual environment in the root directory `venv/` and the required MySQL database with an `alembic_version` table for future migrations.

## Dummy Data

```sql
insert into customer (
        name,
        phone,
        email,
        emergency_contact_name,
        emergency_contact_phone,
        signed_up_on
    ) values (
        'Foo Bar',
        '+00 0000 000000',
        'foo@bar.com',
        'Bam Bar',
        '+00 0000 000000',
        '2024-09-27'
    );
```

```sql
insert into vet
(name, address, phone)
values
('Chiswick Vet', 'London', '222 222 222');
```

```sql
insert into dog
(name, date_of_birth, is_allowed_treats, is_allowed_off_the_lead, is_allowed_on_social_media, is_neutered_or_spayed, behavioral_issues, medical_needs, customer_id, vet_id, breed)
values
('Harry', '2020-01-02', 1, 1, 1, 1, 'A bit barky at times', 'Sore legs', 1, 1, 'German Shepherd');
```

```sql
insert into service
(name, description, price, duration, is_active)
values
('1-hr dog walk', 'A lovely dog walk through the park for an hour!', 25.00, 60.0, 1);
```

## Useful SQL Queries

### Select Bookings

```sql
   select b.date, b.time, c.name, s.name, s.duration
     from booking as b
left join service as s
       on b.service_id = s.id
left join customer as c
       on b.customer_id = c.id
    where b.user_id = 3
      and b.date > '2024-08-31'
      and b.date < '2024-10-01'
 order by b.date asc;
```

### Select Customer, Dog and Vet Names

```sql
   select c.name as customer_name, d.name as dog_name, v.name as vet_name
     from dog as d
left join customer as c
       on d.customer_id = c.id
left join vet as v
       on d.vet_id = v.id
 order by c.name;
```

## Running the App

Set the following environment variables:

| Variable | Description |
| :------- | :---------- |
| DATABASE_PASSWORD | |
| DATABASE_USERNAME | |
| LOGURU_LEVEL | The logger level, see https://loguru.readthedocs.io/en/stable/api/logger.html |
| MAIL_DEFAULT_SENDER_NAME | |
| MAIL_PASSWORD | |
| MAIL_PORT | |
| MAIL_SERVER | |
| MAIL_USE_SSL | |
| MAIL_USE_TLS | |
| MAIL_USERNAME | |
| REMEMBER_COOKIE_DURATION | |
| WEBSITE_LTD_NAME | |
| WEBSITE_NAME | |
| WEBSITE_SLOGAN | |
| WEBSITE_TELEPHONE | |
| WEBISTE_ADDRESS | |
| WEBSITE_INSTAGRAM | |
| WEBSITE_NOSTR | |
| WEBSITE_URL | |

Run locally using:

```bash
bash scripts/wsgi.sh <optional host> <optional port>
```

## Pushing & Deploying

Add the file you want to deploy (e.g. `git add <file to add>`) and commit it (e.g. `git commit -m "<message for commit>"`) then:

```bash
bash scripts/gandi.sh -pd
```

Get help on the usage of this script as follows:

```bash
bash scripts/gandi.sh -u
```

```
Gandi installation & development script.

Syntax: install.sh [-d|h]
options:
i     Initialize gandi and github remote repositories.
p     Push to remote repositories.
d     Deploy to gandi instance.
u     Print this help for usage.
```

## Migrations

After pushing and deploying to the remote server, SSH into the remote server and then:

```bash
cd /srv/data/web/vhosts/default/
bash scripts/migrate <optional migration message>
```

Make sure the `alembic_version` table is generated correctly by running the migration script outlined above:

```bash
bash scripts/migrate init
```

## Reset Logs

SSH into the remote server and then:

```bash
cd /srv/data/var/log/www/
echo "" > uwsgi.log
```

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
