import requests
from requests import Request, Session
import vimeo
from datetime import datetime

secrets = {
    'VIMEO_PATH' :"albums/*****************/",
    'VIMEO_ACCESS_TOKEN' : "*********************",
    'VIMEO_CLIENT_ID' :"*********************",
    'VIMEO_CLIENT_SECRET' : "*******************",
    'GITHUB_ACCESS_TOKEN' : "*******************",
}

def triggerBuild():
    url = 'https://api.github.com/repos/goulchen/picaro_gat/dispatches'
    headers = {'Authorization': 'token ' +  secrets['GITHUB_ACCESS_TOKEN']}
    req = requests.post(url, headers=headers, json={"event_type": "build"})
    if req.status_code != 200 :
        raise ConnectionError('Connection to GitHub Action api failed')
    return req

def getLastGithubWorkflowRun():
    url = 'https://api.github.com/repos/goulchen/picaro_gat/actions/workflows/main.yml/runs'
    res = requests.get(url)
    if res.status_code == 200 and res.content:
        data = res.json()
        if int(data['total_count']) != 0:
            for run in data['workflow_runs']:
                if run["status"] == "in_progress":
                    return 0
                if run["conclusion"] == "success":
                    return run["run_started_at"]
        return 1
    else :
        raise ConnectionError('Connection to api failed')

def getLastVimeoModification():
    
    PATH = secrets['VIMEO_PATH']
    ACCESS_TOKEN = secrets['VIMEO_ACCESS_TOKEN']
    CLIENT_ID =secrets['VIMEO_CLIENT_ID']
    CLIENT_SECRET = secrets['VIMEO_CLIENT_SECRET']

    v = vimeo.VimeoClient(
        token=ACCESS_TOKEN,
        key=CLIENT_ID,
        secret=CLIENT_SECRET
    )
    videosData = v.get('/me/' + PATH)
    if videosData.status_code == 200:
        return videosData.json()['modified_time']
    else :
        raise ConnectionError('Connection to vimeo api failed', videosData.status_code, videosData.text)
    return

def main():
    lastGithubWorkflow =  getLastGithubWorkflowRun()
    if lastGithubWorkflow == 0 :
        return
    if lastGithubWorkflow == 1 :
        triggerBuild()
        return
    lastGithubWorkflow =  datetime.strptime(lastGithubWorkflow,'%Y-%m-%dT%H:%M:%SZ')
    vimeoModification = getLastVimeoModification()
    lastVimeoModification =  datetime.strptime(vimeoModification,'%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
    triggeringBuild = lastGithubWorkflow < lastVimeoModification
    timestring = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if triggeringBuild :
        triggerBuild()
        print(1)
        return
    else:
        print(0)
        return
main()