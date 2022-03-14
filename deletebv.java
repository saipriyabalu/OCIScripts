import com.oracle.bmc.ConfigFileReader;
import com.oracle.bmc.auth.AuthenticationDetailsProvider;
import com.oracle.bmc.auth.ConfigFileAuthenticationDetailsProvider;
import com.oracle.bmc.core.BlockstorageClient;
import com.oracle.bmc.core.model.*;
import com.oracle.bmc.core.requests.*;
import com.oracle.bmc.core.responses.*;
import net.minidev.json.JSONUtil;

import javax.xml.bind.SchemaOutputResolver;
import java.util.*;


public class VolumeBackups {
    public static void main(String[] args) throws Exception {

        final ConfigFileReader.ConfigFile configFile = ConfigFileReader.parseDefault();
        final AuthenticationDetailsProvider provider = new ConfigFileAuthenticationDetailsProvider(configFile);

        BlockstorageClient client = new BlockstorageClient(provider);

        ListVolumeBackupsRequest listVolumeBackupsRequest = ListVolumeBackupsRequest.builder()
                .compartmentId("")
                .limit(1000)
                .sortBy(ListVolumeBackupsRequest.SortBy.Timecreated)
                .sortOrder(ListVolumeBackupsRequest.SortOrder.Desc)
                .lifecycleState(VolumeBackup.LifecycleState.Available).build();

        ListVolumeBackupsResponse response = client.listVolumeBackups(listVolumeBackupsRequest);

        List<VolumeBackup> list =  response.getItems();
        for(VolumeBackup v:list){
            System.out.println("Volume Name: " + v.getDisplayName());
            System.out.println("Time Created: " + v.getTimeCreated());
            Date date = new Date();
            long diffInMillies = date.getTime() - v.getTimeCreated().getTime();
            long difference_In_Days = (diffInMillies / (1000 * 60 * 60 * 24)) % 365;
            System.out.println("Difference in Days: " + difference_In_Days);
            if(difference_In_Days > 30)
            {
                System.out.println("delete the volume");
                deleteVolume(client, v.getId());
            }
            else
                System.out.println("keep the volume");
        }
    }

    private static void deleteVolume(BlockstorageClient client, String id){

        DeleteVolumeBackupRequest deleteVolumeBackupRequest = DeleteVolumeBackupRequest.builder()
                .volumeBackupId(id).build();

        DeleteVolumeBackupResponse response = client.deleteVolumeBackup(deleteVolumeBackupRequest);
    }


}
