create or replace TRIGGER ddl_trigger
BEFORE ddl -- CREATE OR ALTER OR DROP
ON SCHEMA

/* @2022-08-29
 * - kreirana ddl_log tablica i dll_trigger
 * @2024-01-23
 * - zamjena CREATE OR ALTER OR DROP sa DDL
 * - zamjena "IF oper IN ('CREATE', 'DROP', 'ALTER') THEN" sa "IF 1=1 THEN"
 */

DECLARE
  oper ddl_log.operation%TYPE;
  sql_text ora_name_list_t;
  i        PLS_INTEGER;

  l_session_user varchar2(255 char);
  l_session_host varchar2(255 char);
  l_ip_address varchar2(255 char);
  l_module varchar2(255 char);
  l_os_user varchar2(255 char);
  l_server_host varchar2(255 char);
  l_service_name varchar2(255 char);
  l_session_userid varchar2(255 char);
  l_sessionid varchar2(255 char);
  l_sid varchar2(255 char);
  l_terminal varchar2(255 char);
  l_statementid varchar2(255 char);

  l_sql_text clob;
  l_tbl_ddl_before_drop clob;

BEGIN
  -- izvadi tip operacije: create, alter, drop
  SELECT ora_sysevent
  INTO oper
  FROM dual;

  -- izvadi parametre sjednice: os_user, ip_address,...
  BEGIN
    SELECT 
      SYS_CONTEXT ('USERENV', 'SESSION_USER') as session_user,
      SYS_CONTEXT ('USERENV', 'HOST') as session_host,
      SYS_CONTEXT ('USERENV', 'IP_ADDRESS') as IP_ADDRESS,
      SYS_CONTEXT ('USERENV', 'MODULE') as MODULE,
      SYS_CONTEXT ('USERENV', 'OS_USER') as OS_USER,
      SYS_CONTEXT ('USERENV', 'SERVER_HOST') as SERVER_HOST,
      SYS_CONTEXT ('USERENV', 'SERVICE_NAME') as SERVICE_NAME,
      SYS_CONTEXT ('USERENV', 'SESSION_USERID') as SESSION_USERID,
      SYS_CONTEXT ('USERENV', 'SESSIONID') as SESSIONID,
      SYS_CONTEXT ('USERENV', 'SID') as SID,
      SYS_CONTEXT ('USERENV', 'TERMINAL') as TERMINAL,
      SYS_CONTEXT ('USERENV', 'STATEMENTID') as STATEMENTID
    into
      l_session_user,
      l_session_host,
      l_ip_address,
      l_module,
      l_os_user,
      l_server_host,
      l_service_name,
      l_session_userid,
      l_sessionid,
      l_sid,
      l_terminal,
      l_statementid
    FROM DUAL;
  exception when others then null;
  END;

  -- koliko dll ima linija (nisu to i linije teksta nužno)
  i := sql_txt(sql_text);
  --n := ora_sql_txt(sql_text);

  -- izvadi sve linije od DDL-a i spremi ih
  FOR sql_line IN 1..i LOOP
    l_sql_text := l_sql_text || sql_text(sql_line);
  END LOOP;

  -- zalogiraj operaciju
  --IF oper IN ('CREATE', 'DROP', 'ALTER') THEN
  if 1=1 then
    if oper = 'DROP' and ora_dict_obj_type = 'TABLE' then
      begin
        select dbms_metadata.get_ddl('TABLE',ora_dict_obj_name) into l_tbl_ddl_before_drop from dual;
      exception when others then 
        l_tbl_ddl_before_drop := dbms_utility.format_error_stack;
      end;
    end if;

    INSERT INTO ddl_log (
      OPERATION,
      obj_type,
      OBJ_OWNER,
      OBJECT_NAME,
      SQL_TEXT,
      tbl_ddl_before_drop,
      ATTEMPT_BY,
      ATTEMPT_DT,
      session_user,
      session_host,
      ip_address,
      module,
      os_user,
      server_host,
      service_name,
      session_userid,
      sessionid,
      sid,
      terminal,
      statementid
    )
    SELECT 
      ora_sysevent as operation, 
      ora_dict_obj_type as obj_type,
      ora_dict_obj_owner as obj_owner,
      ora_dict_obj_name as object_name,
      l_sql_text  as sql_text, --sql_text(1)
      l_tbl_ddl_before_drop,
      USER as attempt_by,
      SYSDATE as attempt_dt,
      l_session_user,
      l_session_host,
      l_ip_address,
      l_module,
      l_os_user,
      l_server_host,
      l_service_name,
      l_session_userid,
      l_sessionid,
      l_sid,
      l_terminal,
      i --l_statementid
    FROM dual;
  ELSIF oper = 'ALTER' THEN
--    INSERT INTO ddl_log
--    SELECT ora_sysevent, ora_dict_obj_owner,
--    ora_dict_obj_name, sql_text(1), USER, SYSDATE
--    FROM sys.gv_$sqltext
--    WHERE UPPER(sql_text) LIKE 'ALTER%'
--    AND UPPER(sql_text) LIKE '%NEW_TABLE%';
    null;
  END IF;
exception when others then
  null;
END ddl_trigger;
