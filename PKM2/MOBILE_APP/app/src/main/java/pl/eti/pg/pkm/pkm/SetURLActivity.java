package pl.eti.pg.pkm.pkm;

import android.content.Intent;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.EditText;

import org.androidannotations.annotations.Click;
import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.ViewById;

import static pl.eti.pg.pkm.pkm.DataPassingMessages.URLActivityAddress;
import static pl.eti.pg.pkm.pkm.DataPassingMessages.URLActivityPort;

@EActivity(R.layout.activity_set_url)
public class SetURLActivity extends AppCompatActivity {

    @ViewById(R.id.adress)
    protected EditText address;

    @ViewById(R.id.port)
    protected EditText port;

    @Click(R.id.set_settings)
    protected void start_main_activity(){
        String url = address.getText().toString();
        String httpPort = port.getText().toString();
//        SettingsActivity_.intent(this).start();
        final Intent intent = new Intent(this, MainActivity.class);
        intent.putExtra(URLActivityAddress, url);
        intent.putExtra(URLActivityPort, httpPort);
        startActivity(intent);
    }

}
