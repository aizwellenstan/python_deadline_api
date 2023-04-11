"""
This script will submit current file to deadline for render
"""
import os
import sys
import subprocess
import json

def job_info(info_txt):
    job_info_file = r'{}\job_info.job'.format(os.getenv('TEMP'))
    with open(job_info_file, 'w') as job_file:
        job_file.write(info_txt)
    return job_info_file

def plugin_info(info_txt):
    plugin_info_file = r'{}\plugin_info.job'.format(os.getenv('TEMP'))
    with open(plugin_info_file, 'w') as job_file:
        job_file.write(info_txt)
    return plugin_info_file

def submit_to_deadline(job_info_txt, plugin_info_txt):
    # Change deadline exe root
    deadline_cmd = r"C:\Program Files\Thinkbox\Deadline10\bin\deadlinecommand.exe"
    job_file = job_info(job_info_txt)
    info_file = plugin_info(plugin_info_txt)
    command = '{deadline_cmd} "{job_file}" "{info_file}"'.format(**vars())
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    lines_iterator = iter(process.stdout.readline, b"")
    #  Lets print the output log to see the Error / Success 
    for line in lines_iterator:
        print(line)
        sys.stdout.flush()

def GetInfoTxtMayaAss(name, cmd, pool="nuke", priority=60, machineLimit=30):
    job_info_txt = ("MachineLimit=%s\nGroup=maya_2020\nName=%s\nOverrideTaskExtraInfoNames=False\nPlugin=CommandLine\nPool=%s\nPriority=%s\nSecondaryPool=all\nUserName=%s\n") % (machineLimit,name,pool,priority,os.environ.get("USERNAME"))

    executable = cmd.split()[0]
    arg = cmd.replace(executable,'')
    plugin_info_txt = "Executable=%s\nArguments=%s\nShell=default\nShellExecute=False\nSingleFramesOnly=False\n"%(executable,arg)

    return str(job_info_txt.strip()), str(plugin_info_txt)
