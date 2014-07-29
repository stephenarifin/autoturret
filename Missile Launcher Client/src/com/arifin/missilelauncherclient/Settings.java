package com.arifin.missilelauncherclient;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.Switch;

public class Settings extends Activity {

	private Button saveButton;
	private Switch autoAimSwitch;
	private Switch autoScanSwitch;
	
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.settings);
		
		saveButton = (Button)findViewById(R.id.saveButton);
		autoAimSwitch = (Switch)findViewById(R.id.autoAimSwitch);
		autoScanSwitch = (Switch)findViewById(R.id.autoScanSwitch);
		
		saveButton.setOnClickListener(new OnClickListener(){

			public void onClick(View v) {
				Remote.commandQueue.add("connected");
				if(autoAimSwitch.isChecked())
					Remote.commandQueue.add("auto on");
				else
					Remote.commandQueue.add("auto off");
				if(autoScanSwitch.isChecked())
					Remote.commandQueue.add("scan on");
				else
					Remote.commandQueue.add("scan off");
				
				finish();
				
			}
			
		});
	}
}
