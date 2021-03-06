BEGIN_FUNCTION_MAP
	.Func,EUREXKOSPI200옵션선물현재가(시세)조회(t2830),t2830,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t2830InBlock,기본입력,input;
	begin
		단축코드,focode,focode,char,8;
	end
	t2830OutBlock,출력,output;
	begin
		한글명,hname,hname,char,20;
		현재가,price,price,float,6.2;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,float,6.2;
		전일종가,jnilclose,jnilclose,float,6.2;
		등락율,diff,diff,float,6.2;
		거래량,volume,volume,long,12;
		거래대금,value,value,long,12;
		시가,open,open,float,6.2;
		고가,high,high,float,6.2;
		저가,low,low,float,6.2;
		기준가,recprice,recprice,float,6.2;
		이론가,theoryprice,theoryprice,float,6.2;
		행사가,actprice,actprice,float,6.2;
		내재가치,impv,impv,float,6.2;
		시간가치,timevl,timevl,float,6.2;
		KOSPI200지수,kospijisu,kospijisu,float,6.2;
		KOSPI200전일대비구분,kospisign,kospisign,char,1;
		KOSPI200전일대비,kospichange,kospichange,float,6.2;
		KOSPI200등락율,kospidiff,kospidiff,float,6.2;
		CME야간선물현재가,cmeprice,cmeprice,float,6.2;
		CME야간선물전일대비구분,cmesign,cmesign,char,1;
		CME야간선물전일대비,cmechange,cmechange,float,6.2;
		CME야간선물등락율,cmediff,cmediff,float,6.2;
		CME야간선물종목코드,cmefocode,cmefocode,char,8;
		정규장상한가,uplmtprice,uplmtprice,float,6.2;
		정규장하한가,dnlmtprice,dnlmtprice,float,6.2;
		단축코드,focode,focode,char,8;
		예상체결가,yeprice,yeprice,float,6.2;
		전일대비구분,ysign,ysign,char,1;
		전일대비,ychange,ychange,float,6.2;
		등락율,ydiff,ydiff,float,6.2;
		단일가호가여부,danhochk,danhochk,char,1;
	end
	END_DATA_MAP
END_FUNCTION_MAP

