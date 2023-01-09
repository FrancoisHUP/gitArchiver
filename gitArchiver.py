import subprocess
import sys
import os

def archiver(gitDirPath,silence,force,delete) :

    # list of branche you dont want to archive 
    branchToKeepList = ["appro", "master"]

    # Character that can cause troubble when globing
    charBlackList = ["*"]

    # get branches list
    stringOfBranches = subprocess.check_output('cd ' + gitDirPath + " & " + " git branch", shell=True)
    branches = stringOfBranches.split()

    for branch in branches : 
        branchName = branch.decode("utf-8") 
        if branchName not in branchToKeepList and not any([char in branchName for char in charBlackList]):
            error = False
            # archive 
            try : 
                archiveCmd = 'cd ' + gitDirPath + " & " + " git tag archive/" + branchName + " " + branchName
                if not silence :
                    print("$ " + archiveCmd)
                subprocess.check_output(archiveCmd, shell=True)   
            except :
                error = True
                if not delete :
                    print("Could not delete branch " + branchName + ", use -d to force delete.")
            finally :
                if not error or delete: 
                    # delete
                    try : 
                        argDelete = " -D " if force else " -d "
                        deleteBranchCmd = 'cd ' + gitDirPath + " & " + " git branch" + argDelete + branchName
                        if not silence :
                            print("$ " + deleteBranchCmd)
                        subprocess.check_output(deleteBranchCmd, shell=True)
                    except : 
                        print("Something went wrong.")
    # Instructions 
    if not silence :
        print("\n To see the list of archive branch : ")
        print("\n   $ git tag")
        print("\n To undo archive of a branch : ")
        print("\n   $ git checkout -b <branchname> archive/<branchname>")

def main() :
    if len(sys.argv) < 2 : 
        print("py archiveBranches.py <gitSourcePathDirectory> [args]")
        print("Posible args : ")
        print("  -s or --silence : will silence output")
        print("  -f or --force : will delete branch(es) if it's not merge yet (equivalent at git branch -D <branch name>")
        print("  -d of --delete : will force to delete branch(es) event if the same name appear in the archive.")
    else :
        # ARGS
        # source path of git repository
        gitDirPath = os.path.normpath(sys.argv[1])

        # will silence output
        silence = ("-s" or "--silence") in str(sys.argv)

        # will delete if branch is not merge yet
        force = ("-f" or "--force") in str(sys.argv)

        # will force delete branch allready existing archive
        delete = ("-d" or "--delete") in str(sys.argv)

        archiver(gitDirPath,silence,force,delete)

if __name__=='__main__' : 
    main()