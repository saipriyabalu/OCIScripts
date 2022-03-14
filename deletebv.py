import oci
from datetime import datetime,timedelta

config = oci.config.from_file("~/.oci/config","DEFAULT")

# Initialize service client with default config file
core_client = oci.core.BlockstorageClient(config)
ocicompartment="<<enter compartment id>>"

# Send the request to service, some parameters are not required, see API
# LIST VOLUMES
list_volumes_response = core_client.list_volumes(
    compartment_id=ocicompartment,
    availability_domain="CISk:US-ASHBURN-AD-1",
    limit=903,
    sort_by="TIMECREATED",
    sort_order="DESC",
)

# List all the volumes
#print(list_volumes_response.data)
l = len(list_volumes_response.data)
# print(l)

# For each volume id - delete the volume backup
for i in range(0,l):
    print("Backup for the Volume -" + list_volumes_response.data[i].display_name + " will be deleted")
    list_volume_backups_response = core_client.list_volume_backups(
        compartment_id=ocicompartment,
        volume_id=list_volumes_response.data[i].id,
        limit=156,
        sort_by="TIMECREATED",
        sort_order="DESC",
        lifecycle_state="AVAILABLE"
    )
    # LIST VOLUME BACKUP FOR THE VOLUME ID
    print(list_volume_backups_response.data)
    volBackupsLen= len(list_volume_backups_response.data)
    j=0
    # Delete backups greater than 30 days
    for j in range(0,volBackupsLen):
        # print("Date - "+str(list_volume_backups_response.data[j].time_created))
        # print(backuptime)
        # print(timebefore30days)
        timebefore30days = datetime.now() - timedelta(days=30)
        volbackuptime = datetime.strptime(str(list_volume_backups_response.data[j].time_created),
                                       '%Y-%m-%d %H:%M:%S.%f+00:00')

        if timebefore30days > volbackuptime:
            print("Delete backups greater than 30 days")
            print("Deleting volume -" + list_volume_backups_response.data[j].display_name)
            delete_volume_backup_response = core_client.delete_volume_backup(
                volume_backup_id=list_volume_backups_response.data[j].id
            )
            # Get the data from response
            print(delete_volume_backup_response.headers)
        #
        # else:
        #     print("No backups or All backups are created less than 30 days")
