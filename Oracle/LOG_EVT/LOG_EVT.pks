create or replace PACKAGE "LOG_EVT" AS

  -- LOG_START --
  -- l_log_evt_id := LOG_EVT.LOG_START ( p_evt_name => 'p_evt_name', p_table_name =>  'p_table_name', p_info =>  'p_info', p_clob =>  'null' );
  FUNCTION LOG_START (
    p_evt_name in varchar2,
    p_table_name in varchar2:=null,
    p_info in varchar2:=null,
    p_clob in clob:= null
  ) return number;

  -- LOG_END --
  -- LOG_EVT.LOG_END ( p_evt_id => l_log_evt_id, p_row_count => SQL%rowcount, p_info =>  'p_info');
  PROCEDURE LOG_END (p_evt_id in int, p_row_count int:=null, p_info in varchar2:=null);

  -- LOG_ERROR --
  -- LOG_EVT.LOG_ERROR ( p_evt_id => l_log_evt_id);
  PROCEDURE LOG_ERROR (p_evt_id in int);
  
  ----------------------------
  -- timestamp_diff_seconds --
  ----------------------------
  -- FUNKCIJA VRAĆA TRAJANJE U SEKUNDAMA A PRIMA DVA TIMESTAMPA (Pocetka i kraja preocesa)
  function timestamp_diff_seconds (END_TIME timestamp, BEGIN_TIME timestamp) return number;


/*
DECLARE
  LOG_ID INT;
BEGIN
  LOG_ID := HRAGSL.LOG_eVT.LOG_START('TEST');
  HRAGSL.LOG_eVT.LOG_END(LOG_ID, 0, 'TEST');
EXCEPTION WHEN OTHERS THEN
  HRAGSL.LOG_eVT.LOG_END(LOG_ID);
END;
*/

END log_evt;
