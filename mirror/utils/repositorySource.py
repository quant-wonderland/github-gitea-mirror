#!/usr/bin/env python
# https://github.com/PyGithub/PyGithub
from .helper import (
    isBlacklistedRepository,
    log,
    getConfig,
    giteaCreateUserOrOrg,
    giteaSetRepoTopics,
    giteaSession,
    giteaCreateRepo,
    ghApi,
    giteaCreateOrg,
    giteaGetUser,
    config,
    giteaUpdateMirror,
)
from github import GithubException
import time


def repositorySource():
    config = getConfig()
    repo_map = config["repomap"]
    gh = ghApi()
    loop_count = 0
    synced_repos = 0
    updated_repos = 0

    # 获取用户所属的所有组织
    user_orgs = gh.get_user().get_orgs()

    # 遍历用户所属的每个组织
    for org in user_orgs:
        print(f"正在处理组织: {org.login}")
        org_synced_repos = 0
        org_updated_repos = 0
        # 获取组织的所有仓库，包括fork的仓库
        for repo in org.get_repos():
            loop_count += 1
            real_repo = repo.name
            gitea_dest_user = org.login
            repo_owner = org.login

            log("Source Repository : {0}".format(repo.full_name))

            if isBlacklistedRepository(repo.full_name):
                print("     ---> Warning : Repository Matches Blacklist")
                continue

            if real_repo in repo_map:
                gitea_dest_user = repo_map[real_repo]

            gitea_uid = giteaGetUser(gitea_dest_user)

            if gitea_uid == "failed":
                gitea_uid = giteaCreateUserOrOrg(gitea_dest_user, "Organization")

            repo_name = "{0}".format(real_repo)

            m = {
                "repo_name": repo_name,
                "description": (repo.description or "not really known")[:255],
                "clone_addr": repo.clone_url,
                "mirror": True,
                "private": repo.private,
                "uid": gitea_uid,
            }

            status = giteaCreateRepo(m, repo.private, True)
            if status != "failed":
                try:
                    if status == "exists":
                        # 如果仓库已存在，尝试更新镜像
                        update_status = giteaUpdateMirror(gitea_dest_user, repo_name)
                        if update_status == "success":
                            updated_repos += 1
                            org_updated_repos += 1
                            print(f"成功更新仓库: {repo.full_name}")
                        else:
                            print(f"更新仓库失败: {repo.full_name}")
                    else:
                        topics = repo.get_topics()
                        giteaSetRepoTopics(repo_owner, repo_name, topics)
                        synced_repos += 1
                        org_synced_repos += 1
                        print(f"成功同步仓库: {repo.full_name}")
                except GithubException as e:
                    print("###[error] ---> Github API Error Occured !")
                    print(e)
                    print(" ")
            else:
                log(repo)

            if loop_count % 50 == 0:
                log(False)
                log("Time To Sleep For 5 Seconds")
                log(False)
                time.sleep(5)
            else:
                log(False)

        print(
            f"组织 {org.login} 同步完成，新同步 {org_synced_repos} 个仓库，更新 {org_updated_repos} 个仓库"
        )

    print(
        f"所有组织同步完成，总共新同步 {synced_repos} 个仓库，更新 {updated_repos} 个仓库"
    )
