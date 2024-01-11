int batt_check(){
  return 0;
  double batt = io_get_batt();
  if(batt >= BATT_MIN){
    return 0;
  }
  else{
    Serial.print("low battery = ");
    Serial.println(batt);
    run_ctrl_set(STP, 0, 0);
    return -1;
  }
}
