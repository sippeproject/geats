module MCollective
  module Agent
    class Geats < RPC::Agent
      action 'define' do
        implemented_by "/home/rmt/code/sippe/geats/bin/mcagent.py"
      end
      action 'start' do
        implemented_by "/home/rmt/code/sippe/geats/bin/mcagent.py"
      end
      action 'stop' do
        implemented_by "/home/rmt/code/sippe/geats/bin/mcagent.py"
      end
      action 'shutdown' do
        implemented_by "/home/rmt/code/sippe/geats/bin/mcagent.py"
      end
      action 'undefine' do
        implemented_by "/home/rmt/code/sippe/geats/bin/mcagent.py"
      end
      action 'info' do
        implemented_by "/home/rmt/code/sippe/geats/bin/mcagent.py"
      end
      action 'status' do
        implemented_by "/home/rmt/code/sippe/geats/bin/mcagent.py"
      end
      action 'migrate' do
        implemented_by "/home/rmt/code/sippe/geats/bin/mcagent.py"
      end
    end
  end
end
