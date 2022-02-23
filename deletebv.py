
import oci
from datetime import datetime


config = oci.config.from_file("~/.oci/config","DEFAULT")

# Initialize service client with default config file
core_client = oci.core.BlockstorageClient(config)
ocicompartment="ocid1.compartment.oc1..aaaaaaaa77nal23ijjj6bzlzj7onsgn4txw6g5y62j6xfeypptgbc242tttq"

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
    for j in range(0,volBackupsLen):
        # date_time_obj = datetime.strptime(list_volume_backups_response.data[j].time_created, '%d/%m/%y %H:%M:%S')
        # #timecreated= list_volume_backups_response.data[j].time_created
        # #startdate=list_volume_backups_response.data[j].time_created.getTime()
        # #startdate = datetime.datetime.now(datetime.timezone.utc).isoformat() - list_volume_backups_response.data[j].time_created
        # print(date_time_obj)

        #print(timecreated)
        print(datetime.datetime.now(datetime.timezone.utc).isoformat())
        print("Deleting volume -" + list_volume_backups_response.data[j].display_name)
        delete_volume_backup_response = core_client.delete_volume_backup(
            volume_backup_id=list_volume_backups_response.data[j].id
        )

        # Get the data from response
        print(delete_volume_backup_response.headers)
