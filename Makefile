.PHONY:all install active clean

SPIRDER_ROOT=$(shell pwd)
export PATH:=$(SPIRDER_ROOT)/.virtualenv/bin:./bin:./lib:$(PATH)

all: clean install

install: basic

basic:
	/usr/local/bin/virtualenv $(SPIRDER_ROOT)/.virtualenv
	$(SPIRDER_ROOT)/.virtualenv/bin/pip install -r $(SPIRDER_ROOT)/requirments.txt

# # 请手动激活沙盒环境
# active:
# 	source $(TTP-TEST-ROOT)/.virtualenv/bin/active

# # 请手动关闭沙盒环境
# deactive:
# 	$(TTP-TEST-ROOT)/.virtualenv/bin/deactive

clean:
	rm -rf $(SPIRDER_ROOT)/.virtualenv
