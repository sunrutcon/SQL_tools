create or replace PACKAGE BODY         "LOG_EVT" AS

  ---------------
  -- LOG_START --
  ---------------
  FUNCTION LOG_START (p_evt_name in varchar2, p_table_name in varchar2:=null, p_info in varchar2:=null, p_clob in clob:= null) return number AS
    l_evt_id int;
    l_clob_id int;
    PRAGMA AUTONOMOUS_TRANSACTION;
  begin

    if p_clob is not null then
      insert into CLOB_LOG (EVT_NAME, LOG_CLOB) values (substr(p_evt_name,1,128), p_clob) returning id into l_clob_id;
      null;
    end if;

    INSERT INTO EVT_LOG (id, evt_name, table_name, INFO_MESSAGE, clob_id)
    values (SEQ_EVT_LOG.nextval, p_evt_name, p_table_name, substr(p_info,1,500), l_clob_id) returning id into l_evt_id;
    COMMIT;

    return l_evt_id;
  END LOG_START;

  ---------------
  -- LOG_END --
  ---------------
  PROCEDURE LOG_END (p_evt_id in int, p_row_count int:=null, p_info in varchar2:=null) AS
    l_end_time timestamp;
    l_begin_time timestamp;
    l_duration_sec number(20,6);
    PRAGMA AUTONOMOUS_TRANSACTION;
  begin
    l_end_time:=systimestamp;

    UPDATE EVT_LOG
    SET DATETIME_END = l_end_time,
        duration_sec = timestamp_diff_seconds(l_end_time,DATETIME_START),
        STATUS='OK',
        ROW_COUNT = p_row_count,
        INFO_MESSAGE = substr(INFO_MESSAGE || p_info || ' [duration: ' || to_char(l_end_time-DATETIME_START) || ']',1,500)
    where ID = p_evt_id;

    commit;
  END LOG_END;

  ---------------
  -- LOG_ERROR --
  ---------------
  PROCEDURE LOG_ERROR (p_evt_id in int) AS
    l_end_time timestamp;
    l_begin_time timestamp;
    l_duration_sec number(20,6);
    PRAGMA AUTONOMOUS_TRANSACTION;
  begin
    l_end_time:=systimestamp;

    UPDATE EVT_LOG
    SET DATETIME_END = l_end_time,
        duration_sec = timestamp_diff_seconds(l_end_time,DATETIME_START),
        STATUS='ERROR',
        ERROR_MESSAGE=substr(DBMS_UTILITY.format_error_stack||chr(10)||chr(10)||DBMS_UTILITY.FORMAT_ERROR_BACKTRACE,1,2000)
    where ID=p_evt_id;

    commit;
  END LOG_ERROR;
  
  ----------------------------
  -- timestamp_diff_seconds --
  ----------------------------
  -- FUNKCIJA VRAĆA TRAJANJE U SEKUNDAMA A PRIMA DVA TIMESTAMPA (Pocetka i kraja preocesa)
  function timestamp_diff_seconds (END_TIME timestamp, BEGIN_TIME timestamp) return number is 
  begin
    return extract (day    from (END_TIME-BEGIN_TIME))*24*60*60 +
           extract (hour   from (END_TIME-BEGIN_TIME))*60*60+
           extract (minute from (END_TIME-BEGIN_TIME))*60+
           extract (second from (END_TIME-BEGIN_TIME));
  end;

END LOG_EVT;
