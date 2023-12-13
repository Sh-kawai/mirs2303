/*int line_trace(double del){
	int pwm_s, pwm_l, pwm_r;
	int stop;

	int white = 903;	//715, 905
	int brack = 1010;	//965, 989
	int gray = (white + brack)/2.0;
	//int ggray = (gray + brack)/2.0;	//白地用
	//int ggray = (gray + white)/2.0;	//黒地用
	//printf("gray : %d\n", gray);

	request_get_pwm(&pwm_s, &pwm_l, &pwm_r);
	//printf("pwm_s : %d\n", pwm_s);
	//printf("pwm_l : %d\n", pwm_l);
	//printf("pwm_r : %d\n", pwm_r);
	printf("del2 : %f\n", del);

	if(pwm_s <= gray && del >= 1.25){
		stop = 1;
		request_linetrace(4);
	}else{
		printf("pwm_l : %d,pwm_r : %d\n", pwm_l, pwm_r);
		if(pwm_l < gray && pwm_r < gray){
			command_data.val[0] = 5;	//直進
			stop = 0;
			printf("ここまで来てる1");
		}else if(pwm_l >= gray && pwm_r <= gray){	//><白地, <>黒地
			command_data.val[0] = 6;	//右旋回
			stop = 0;
			printf("ここまで来てる2");
		}else if(pwm_l <= gray && pwm_r >= gray){	//<>白地, ><黒地
			command_data.val[0] = 7;	//左旋回
			stop = 0;
			printf("ここまで来てる3");
		}else{
			command_data.val[0] = 4;
			stop = 0;
			printf("ここまで来てる4");
		}
	}
	
	return stop;
}

/*int rotate(double del){
	int pwm_s, pwm_l, pwm_r, pwm_l_sub, pwm_r_sub;
	int stop;

	int white = 869;	//715, 905
	int brack = 1012;	//965, 989
	int gray = (white + brack)/2.0;
	//int ggray = (gray + brack)/2.0;	//白地用
	//int ggray = (gray + white)/2.0;	//黒地用
	//printf("gray : %d\n", gray);

	request_get_pwm(&pwm_s, &pwm_l, &pwm_r);
	request_get_pwm_sub(&pwm_l_sub, &pwm_r_sub);
	//printf("pwm_s : %d\n", pwm_s);
	printf("pwm_l : %d\n", pwm_l);
	printf("pwm_r : %d\n", pwm_r);
	printf("del2 : %f\n", del);

	if(pwm_l <= gray && pwm_r <= gray && pwm_l_sub <= gray && pwm_r_sub <= gray && del >= 1.25){
		stop = 1;
		request_linetrace(4);
	}else{
		request_linetrace(8);	//回転
		stop = 0;
		printf("ここまで来てる5");
	}
	
	return stop;
}*/

/*int rotate(double del){
	int speed, dist;

	printf("del2 : %f\n", del);

	sleep(1);
	speed = 25;
	dist = 5;
	request_set_runmode(STR, speed, dist);
	printf("ここまで来てるよ1\n");
	sleep(5);

	speed = 30;
	dist = -95;
	request_set_runmode(ROT, speed, dist);
	printf("ここまで来てるよ2\n");
	sleep(5);
	
	return 1;
}*/

