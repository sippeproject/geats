module MCollective
  module Agent
    class Geats < RPC::Agent
      def which(cmd)
        exts = ENV['PATHEXT'] ? ENV['PATHEXT'].split(';') : ['']
        ENV['PATH'].split(File::PATH_SEPARATOR).each do |path|
          exts.each { |ext|
            exe = File.join(path, "#{cmd}#{ext}")
            return exe if File.executable? exe
          }
        end
        return nil
      end
      bindir = which("mcagent.py")
      action 'provision' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'define' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'start' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'stop' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'shutdown' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'undefine' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'deprovision' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'info' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'status' do
        implemented_by "#{bindir}/mcagent.py"
      end
      action 'migrate' do
        implemented_by "#{bindir}/mcagent.py"
      end
    end
  end
end
