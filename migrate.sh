#!/bin/bash
set -x
set -e

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

mysql_container_name=firm-db
web_container_name=firm-web
mysql_db=firm
mysql_username=root
mysql_password=123456
media_dir=/firm/media
backup_dir=${parent_path}/backup

backup_dir_date=${backup_dir}/`date +%Y-%m-%d`
backup_date=`date +%Y%m%d-%H%M`


if [ ! -n "$1" ] ;then
    echo -e "\nUsage: migrate [-b] [-c] [-r <*.sql.gz> <*.tar.gz>] [-t <\"0 3 * * *\">]\n"
    echo "  -b,   backup mysql and media"
    echo "  -c,   clean old-to-date backup"
    echo "  -r,   restore mysql and media"
    echo -e "  -t,   set cron schedule expressions\n"
fi


while getopts :bcr:t: opt

do
    case $opt in
        b)
        echo -e "\n-----  Current start Backup  -----"

        echo "1. mkdir backup filedir: ${backup_dir_date}"
        mkdir -p ${backup_dir_date}

        echo "2. Backup MySQL to ${backup_dir_date}"
        docker exec ${mysql_container_name} /usr/bin/mysqldump -u ${mysql_username} --password=${mysql_password} ${mysql_db} | gzip > ${backup_dir_date}/website-${backup_date}.sql.gz

        echo "3. Backup media to ${backup_dir_date}"
#        tar -zcvf  ${backup_dir_date}/media-${backup_date}.tar.gz ${media_dir}
        if [ -z "$(ls -A /tmp/media)" ];then
          echo "/tmp/media 为空目录.................."
        else
          echo "/tmp/media 不为空...................."
          rm -rf /tmp/media
        fi

        docker cp ${web_container_name}:${media_dir} /tmp
        cd /tmp
        tar -zcvf  ${backup_dir_date}/media-${backup_date}.tar.gz media
        rm -rf media
        cd "$parent_path"

        echo -e "-----  Backup Success!  -----\n"
        ;;
        c)
        echo -e "\n-----  Current start Clean  -----"

        echo "1. Remove old-to-date website-*.sql"
        find ${backup_dir} -mtime +1 -name "*.sql.gz" -exec rm -rf {} \;

        echo "2. Remove old-to-date media-*.tar.gz"
        find ${backup_dir} -mtime +1 -name "*.tar.gz" -exec rm -rf {} \;

        echo "3. Remove empty filedir"
        while [ "$(find ${backup_dir} -empty)" ]; do find ${backup_dir} -empty | xargs -i rm -r {}; done

        echo -e "-----  Clean Success!  -----\n"
        ;;
        r)
        backup_sql=$2
        backup_media=$3

        echo -e "\n-----  Current start Restore  -----"

        echo "1. Unzip ${backup_sql}"
        gzip -cd ${backup_sql} > ${backup_sql%.*}

        echo "2. Restore MySQL Databases"
        cat ${backup_sql%.*} | docker exec -i ${mysql_container_name} /usr/bin/mysql -u ${mysql_username} --password=${mysql_password} ${mysql_db}

        echo "3. Restore Media File"
        tar -zxvf ${backup_media} -C /tmp
        docker cp /tmp/media ${web_container_name}:/firm

        echo -e "-----  Restore Done!  -----\n"
        ;;
        t)
        echo "
        $2$3$4$5$6 cd `pwd` && sh migrate.sh -b -c

        " >> /var/spool/cron/root
        echo "Like crontab -e. Set cron schedule expressions: $2$3$4$5$6"
        echo "Command：cd `pwd` && sh migrate.sh -b -c"
        ;;
        ?)
        echo -e "\nUsage: migrate [-b] [-c] [-r <*.sql.gz> <*.tar.gz>] [-t <\"0 3 * * *\">]\n"
        echo "  -b,   backup mysql and media"
        echo "  -c,   clean old-to-date backup"
        echo "  -r,   restore mysql and media"
        echo -e "  -t,   set cron schedule expressions\n"
        exit 1
    esac
done
