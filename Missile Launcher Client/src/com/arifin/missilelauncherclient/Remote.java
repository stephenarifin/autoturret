/*
 * Main Activity Class
 * 
 * This class provides the layout and button interface of the remote
 * and streams the video from the webcam
 * 
 * Made by Stephen Arifin
 * 
 */
package com.arifin.missilelauncherclient;

import java.io.IOException;
import java.net.URI;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;
import android.widget.ImageButton;
import android.widget.ToggleButton;

public class Remote extends Activity {
	
	private static final boolean DEBUG = false;
	private static final String TAG = "MJPEG";

	// Buttons for the remote
	private ImageButton upImageButton;
	private ImageButton downImageButton;
	private ImageButton leftImageButton;
	private ImageButton rightImageButton;
	private ImageButton fireImageButton;
	
	// View for the webcam streamer
	private MjpegView webcamView;
	
	// IP Address and port number for the server on the Beaglebone
//	public static final String SERVER_IP = "coppell.dyndns.org";
	public static final String SERVER_IP = "128.247.107.74";
	public static final int SERVER_PORT = 5005;
	public static final int WEBCAM_PORT = 8090;
	
	final Handler handler = new Handler();
	
	// The HTTP URL that the Beaglebone streams towards
	String webcamStreamURL = "http://" + SERVER_IP + ":" + WEBCAM_PORT + "/?action=stream";
	
	// Image resolution
	// MUST BE THE SAME AS WHAT IS PUT IN launch_webcam.sh or it will crash
	public static final int webcamWidth = 352;
	public static final int webcamHeight = 288;
	
	// The command queue, which is how the Activity class communicates
	// with the SendCommand class
	public static BlockingQueue<String> commandQueue = new LinkedBlockingQueue<String>();
	

	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_remote);
		
		upImageButton = (ImageButton) findViewById(R.id.upImageButton);
		downImageButton = (ImageButton) findViewById(R.id.downImageButton);
		leftImageButton = (ImageButton) findViewById(R.id.leftImageButton);
		rightImageButton = (ImageButton) findViewById(R.id.rightImageButton);
		fireImageButton = (ImageButton) findViewById(R.id.fireImageButton);
		
		webcamView = (MjpegView) findViewById(R.id.webcam);
		
		// If the webcam view has not been instantiated yet
		if(webcamView != null)
			webcamView.setResolution(webcamWidth, webcamHeight);
		
		setTitle(R.string.connecting);
		
		// Creates the network communication thread, passing through
		// the commandQueue
		new Thread(new SendCommand(commandQueue)).start();
		
		// Each button sends a command to the commandQueue, which is then read
		// by the SendCommand class
		upImageButton.setOnTouchListener(new OnTouchListener(){
			
			public boolean onTouch(View v, MotionEvent event) {
				
				switch (event.getAction() & MotionEvent.ACTION_MASK){
				
				case MotionEvent.ACTION_DOWN:
					commandQueue.add("up");
					upImageButton.setImageResource(R.drawable.up_keypad_pressed);
					return true;
				
				case MotionEvent.ACTION_UP:
					commandQueue.add("stop");
					upImageButton.setImageResource(R.drawable.up_keypad);
					return true;
					
				}
				
				return false;
			}
		});
		
		downImageButton.setOnTouchListener(new OnTouchListener(){
			
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				
				switch (event.getAction() & MotionEvent.ACTION_MASK){
				
				case MotionEvent.ACTION_DOWN:
					commandQueue.add("down");
					downImageButton.setImageResource(R.drawable.down_keypad_pressed);
					return true;
				
				case MotionEvent.ACTION_UP:
					commandQueue.add("stop");
					downImageButton.setImageResource(R.drawable.down_keypad);
					return true;
					
				}
				
				return false;
			}
		});

		leftImageButton.setOnTouchListener(new OnTouchListener(){
			
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				
				switch (event.getAction() & MotionEvent.ACTION_MASK){
				
				case MotionEvent.ACTION_DOWN:
					commandQueue.add("left");
					leftImageButton.setImageResource(R.drawable.left_keypad_pressed);
					return true;
				
				case MotionEvent.ACTION_UP:
					commandQueue.add("stop");
					leftImageButton.setImageResource(R.drawable.left_keypad);
					return true;
					
				}
				
				return false;
			}
		});

		rightImageButton.setOnTouchListener(new OnTouchListener(){
			
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				
				switch (event.getAction() & MotionEvent.ACTION_MASK){
				
				case MotionEvent.ACTION_DOWN:
					commandQueue.add("right");
					rightImageButton.setImageResource(R.drawable.right_keypad_pressed);
					return true;
				
				case MotionEvent.ACTION_UP:
					commandQueue.add("stop");
					rightImageButton.setImageResource(R.drawable.right_keypad);
					return true;
					
				}
				
				return false;
			}
		});

		fireImageButton.setOnTouchListener(new OnTouchListener(){
			
			@Override
			public boolean onTouch(View v, MotionEvent event) {
				
				switch (event.getAction() & MotionEvent.ACTION_MASK){
				
				case MotionEvent.ACTION_DOWN:
					commandQueue.add("fire");
					fireImageButton.setImageResource(R.drawable.fire_keypad_pressed);
					return true;
				case MotionEvent.ACTION_UP:
					fireImageButton.setImageResource(R.drawable.fire_keypad);
					return true;
					
				}
				
				return false;
			}
		}); 
	}
	
	// Toggles the turret to either Manual mode or Auto Mode
	public void autoToggle(View view){
		
		boolean autoTurretOn = ((ToggleButton) view).isChecked();
		
//		webcamView.setAutoTurret(autoTurretOn);
		if(autoTurretOn)
			commandQueue.add("auto");
		else
			commandQueue.add("off");

	}
	
	// Sends a command to the server that the client has connected
	public void onStart() {
    	if(DEBUG) Log.d(TAG,"onStart()");
    	
    	commandQueue.add("connected");
    	
    	// Gives the webcam stream time to load
    	try {
			Thread.sleep(3000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
    	// Creates the webcam stream
		new WebcamRead().execute(webcamStreamURL);
    	setTitle(R.string.app_name);
    	
        super.onStart();
    }
    public void onPause() {
    	if(DEBUG) Log.d(TAG,"onPause()");
        super.onPause();
        if(webcamView!=null){
        	if(webcamView.isStreaming()){
		        webcamView.stopPlayback();
        	}
        }
    }
    
    // Turns off the webcam if not in auto mode
    public void onStop() {
    	if(DEBUG) Log.d(TAG,"onStop()");
    	commandQueue.add("stop");
    	commandQueue.add("disconnected");
        super.onStop();
    }

    public void onDestroy() {
    	if(DEBUG) Log.d(TAG,"onDestroy()");
    	
    	if(webcamView!=null){
    		webcamView.freeCameraMemory();
    	}
    	
        super.onDestroy();
    }
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.remote, menu);
		return true;
	}
	
	public boolean onOptionsItemSelected(MenuItem item){
		switch(item.getItemId()){
		case R.id.action_settings:
			Intent intent = new Intent(getApplication(), Settings.class);
			startActivity(intent);
			return true;
		default:
			return super.onOptionsItemSelected(item);
		}
	}
	
	
	
    public void setImageError(){
    	handler.post(new Runnable() {
    		@Override
    		public void run() {
    			setTitle(R.string.image_error);
    			return;
    		}
    	});
    }

	public class WebcamRead extends AsyncTask<String, Void, MjpegInputStream> {
        protected MjpegInputStream doInBackground(String... url) {
            //TODO: if camera has authentication deal with it and don't just not work
            HttpResponse res = null;         
            DefaultHttpClient httpclient = new DefaultHttpClient(); 
            HttpParams httpParams = httpclient.getParams();
            HttpConnectionParams.setConnectionTimeout(httpParams, 5*1000);
            HttpConnectionParams.setSoTimeout(httpParams, 5*1000);
            if(DEBUG) Log.d(TAG, "1. Sending http request");
            try {
                res = httpclient.execute(new HttpGet(URI.create(url[0])));
                if(DEBUG) Log.d(TAG, "2. Request finished, status = " + res.getStatusLine().getStatusCode());
                if(res.getStatusLine().getStatusCode()==401){
                    //You must turn off camera User Access Control before this will work
                    return null;
                }
                return new MjpegInputStream(res.getEntity().getContent());  
            } catch (ClientProtocolException e) {
            	if(DEBUG){
	                e.printStackTrace();
	                Log.d(TAG, "Request failed-ClientProtocolException", e);
            	}
                //Error connecting to camera
            } catch (IOException e) {
            	if(DEBUG){
	                e.printStackTrace();
	                Log.d(TAG, "Request failed-IOException", e);
            	}
                //Error connecting to camera
            }
            return null;
        }

        protected void onPostExecute(MjpegInputStream result) {
            webcamView.setSource(result);
            if(result!=null){
            	result.setSkip(1);
            	setTitle(R.string.app_name);
            }else{
            	setTitle(R.string.disconnected);
            }
            webcamView.setDisplayMode(MjpegView.SIZE_BEST_FIT);
            webcamView.showFps(false);
        }
    }
	
	public class RestartApp extends AsyncTask<Void, Void, Void> {
        protected Void doInBackground(Void... v) {
        	Remote.this.finish();
            return null;
        }

        protected void onPostExecute(Void v) {
        	startActivity((new Intent(Remote.this, Remote.class)));
        }
    }
	
}



