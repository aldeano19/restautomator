import os, sys, time, subprocess
import yaml

SUCCESS = 0

def display_usage():
  print "Import a free style project to a new user's account"
  print "Usage:"
  print "    python tcc_create_suite.py user_id project_id suite_import_directory suite_output_directory"
  print "Example:"
  print "    python tcc_import_project.py 1 2 /mysuite /mynewsuite"
  sys.exit()

def getTitleAndDescFromYaml(step):
  title = "Error"
  desc = "Error"
  f = open(step)
  contents = f.read()
  f.close()
  dictionary = yaml.load(contents)
  
  for key in dictionary:
    if key != 'assert':

      
      print "KEY(step name): ", key
      

      name = key
      desc = dictionary[key]['details']['description']
  return name, desc


def run_testcases(outputDir, newUserId, newProjectId, testcases):
  # testcase bundle looks like ...
  # {"name":"test_case1", "title":"", "desc":"", "ordinal":"1", "abort":"1", "id":"180"}
  tcCtr = 0
  for testcase in testcases:
    tcCtr = tcCtr + 1
    os.chdir(testcase)

    name = testcase
    title = "None"
    desc = "None"
    ordinal = tcCtr 
    testcaseDirName = str(ordinal).zfill(3) + "_000"
    newTestCaseDir = outputDir + "/" + testcaseDirName
    os.mkdir(newTestCaseDir)

    bundle = '{"name":"%s", "desc":"%s", "title":"None", "ordinal":"%s", "abort":"0", "id":"0"}' % (name, desc, ordinal)
    # print "TESTCASE", bundle

    thisFileName = newTestCaseDir + "/bundle"
    f = open(thisFileName, "w")
    f.write(bundle)
    f.close()    

    thisDir = os.listdir('.')
    steps = []
    # create a list of steps for this testcase
    for entry in thisDir:
      if len(entry) > 4 and entry[-4:]:
        steps.append(entry)
    steps.sort()
    rc = run_steps(newTestCaseDir, newUserId, newProjectId, steps)
    os.chdir('..')
  return SUCCESS



def run_steps(newTestCaseDir, newUserId, newProjectId, steps):
  # step dir name is step_001 bla
  # step bundle looks like this ...
  # {"name":"step title", "desc":"step description", "ordinal":"0", "abort":"0", "fail_type":"Error", "execute":"python hello_world.py", "id":"260"}

  stepCtr = 0
  for step in steps:
    
    stepCtr = stepCtr + 1
    print "======================="
    print "STEP: ", step
    try:
      name, desc = getTitleAndDescFromYaml(step)
      print "NAME: ", name
      print "DESC: ", desc
    except:
      print "EXCEPTED!!!!!!!!"

    
    print "======================="

    continue

    ordinal = stepCtr
    abort = 0
    fail_type = 'Error'
    execute = "python tauto.py %s" % (step)

    stepDirName = "step_" + str(ordinal).zfill(3)
    newStepDir = newTestCaseDir + "/" + stepDirName
    os.mkdir(newStepDir)

    bundle = '{"name":"%s", "desc":"%s", "ordinal":"%s", "abort":"0", "fail_type":"Error", "execute":"%s", "id":"0"}' % (name, desc, ordinal, execute)

    thisFileName = newStepDir + "/bundle"
    f = open(thisFileName, "w")
    f.write(bundle)
    f.close()    

    # copy over the yaml file
    newFileName = newStepDir + "/" + step
    cmdStr = "cp %s %s" % (step, newFileName)
    cmdStatus = os.popen(cmdStr).read()

  return SUCCESS

######################
## main entry point ##
######################
if len(sys.argv) < 5:
  display_usage()

# will need newUserId and newProjectId passed in 
# AND have no way to validate them
newUserId = 0
newUserId = sys.argv[1]
newProjectId = sys.argv[2]
projectDir = sys.argv[3]
outputDir = sys.argv[4]

os.chdir(projectDir)

tmpArray = projectDir.split("/")
newSuiteName = tmpArray[len(tmpArray)-1]
name = newSuiteName
desc = 'RAW SUITE CREATED FROM SCRATCH'
ordinal = 1
abort = 0

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

# suite bundle looks like this ...
# {"name":"suite1", "desc":"Suite Description:", "ordinal":"1", "abort":"0", "id":"42"}
bundle = '{"name":"%s", "desc":"%s", "ordinal":"1", "abort":"0", "id":"0"}' % (name, desc)


thisFileName = outputDir + "/bundle"
f = open(thisFileName, "w")
f.write(bundle)
f.close()

thisDir = os.listdir('.')
testcases = []
# first create a list of suites
for entry in thisDir:
  if os.path.isdir(entry):
    testcases.append(entry)

testcases.sort()

rc = run_testcases(outputDir, newUserId, newProjectId, testcases)

