#---------------------------------------------------------------------
# Global settings
#---------------------------------------------------------------------
global
    daemon
    maxconn     512
    user        haproxy
    group       haproxy
    pidfile     /var/run/haproxy.pid

    # turn on stats unix socket
    stats socket /var/lib/haproxy/stats

#---------------------------------------------------------------------
# common defaults that all the 'listen' and 'backend' sections will
# use if not designated in their block
#---------------------------------------------------------------------
defaults
    mode                    http
    option forwardfor       except 127.0.0.0/8
    option                  redispatch
    retries                 3
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client          1m
    timeout server          1m
    timeout check           10s
    maxconn                 512

#---------------------------------------------------------------------
# main frontend which proxys to the backends
#---------------------------------------------------------------------
% for name, frontend in frontends.items():
frontend  ${ name } ${ frontend['binding'] }
    % for (key, value) in frontend.get('options', {}).items():
    ${ key } ${ value }
    % endfor
    
% endfor

#---------------------------------------------------------------------
# round robin balancing between the various backends
#---------------------------------------------------------------------
% for name, backend in backends.items():
backend ${ name }
    % for (key, value) in backend.get('options', {}).items():
	${ key } ${ value }
    % endfor
    
	% for instance in backend.get('instances', []): 
	server ${ instance.id } ${ instance.private_ip_address }
	% endfor
% endfor
