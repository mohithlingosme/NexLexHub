# LexNexHub Phase 1 - Deep Implementation Plan

## Table of Contents
- [Objectives & KPIs](#objectives)
- [Core Workflow](#workflow)
- [Data Sources](#sources)
- [Processing Pipeline](#pipeline)
  - [Scraper Layer](#scraper)
  - [Cleaning](#cleaning)
  - [Filtering](#filtering)
  - [Chunking](#chunking)
  - [LLM Processing](#llm)
topics of content of the fetch 
  a. Title
  b. data and time (just for the sorting the data based on relevance not pratical use for functionality just fetct the right news for the date)
  c. content of the news articles 
sample input 
{
  "url": "https://www.livelaw.in/supreme-court/s1563-crpcs1753-bnss-magistrates-order-for-investigation-cant-be-quashed-by-relying-on-accuseds-defence-supreme-court-530209",
  "title": "Magistrate's Order For Investigation Can't Be Quashed By Relying On Accused's Defence: Supreme Court",
  "content": "The Supreme Court has held that High Courts cannot quash a Magistrate’s order directing investigation under Section 156(3) CrPC or Section 175(3) BNSS by relying on the defence taken by the accused. The Court emphasized that at the stage of ordering investigation, only the allegations in the complaint and the material produced by the complainant are to be considered, and not the defence of the accused. It clarified that if the complaint prima facie discloses a cognizable offence, the Magistrate is justified in directing investigation. The High Court, while exercising its inherent powers, should not conduct a mini-trial or evaluate defence evidence at this preliminary stage, as doing so would improperly interfere with the investigation process. The ruling reinforces that judicial scrutiny at this stage is limited and should not derail legitimate criminal investigation initiated on valid complaints.",
  "date": "2026-04-14T12:59:00+05:30"
}
processed Output expectation 
   a. title 
   b. Summary intro
   c. Background 
   d. Court reasoning 
   e. Legal principles
   f. Case references
   g. Final ruling 
   h. Conclussion 
Sample - 
<html><head><meta content="text/html; charset=UTF-8" http-equiv="content-type"><style type="text/css">ul.lst-kix_cfy6hfjc7ksl-0{list-style-type:none}ul.lst-kix_cfy6hfjc7ksl-3{list-style-type:none}ul.lst-kix_cfy6hfjc7ksl-4{list-style-type:none}ul.lst-kix_cfy6hfjc7ksl-1{list-style-type:none}ul.lst-kix_cfy6hfjc7ksl-2{list-style-type:none}ul.lst-kix_cfy6hfjc7ksl-7{list-style-type:none}ul.lst-kix_cfy6hfjc7ksl-8{list-style-type:none}ul.lst-kix_cfy6hfjc7ksl-5{list-style-type:none}ul.lst-kix_cfy6hfjc7ksl-6{list-style-type:none}.lst-kix_3xsvf8xpqkr-8>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-8}.lst-kix_g6xizdwyjqq3-1>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-1,lower-latin) ". "}.lst-kix_r38jvyodkvi3-0>li:before{content:"\0025cf   "}.lst-kix_g6xizdwyjqq3-0>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-0,decimal) ". "}ul.lst-kix_chmeg86wx98z-8{list-style-type:none}.lst-kix_g6xizdwyjqq3-5>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-5,lower-roman) ". "}.lst-kix_g6xizdwyjqq3-7>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-7,lower-latin) ". "}ul.lst-kix_chmeg86wx98z-7{list-style-type:none}.lst-kix_g6xizdwyjqq3-2>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-2,lower-roman) ". "}.lst-kix_g6xizdwyjqq3-6>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-6,decimal) ". "}ul.lst-kix_chmeg86wx98z-2{list-style-type:none}ul.lst-kix_chmeg86wx98z-1{list-style-type:none}ul.lst-kix_chmeg86wx98z-0{list-style-type:none}.lst-kix_g6xizdwyjqq3-3>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-3,decimal) ". "}ul.lst-kix_chmeg86wx98z-6{list-style-type:none}ul.lst-kix_chmeg86wx98z-5{list-style-type:none}ul.lst-kix_chmeg86wx98z-4{list-style-type:none}.lst-kix_g6xizdwyjqq3-4>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-4,lower-latin) ". "}ul.lst-kix_chmeg86wx98z-3{list-style-type:none}.lst-kix_g6xizdwyjqq3-8>li:before{content:"" counter(lst-ctn-kix_g6xizdwyjqq3-8,lower-roman) ". "}.lst-kix_xuggaj7hom8a-5>li:before{content:"\0025a0   "}.lst-kix_xuggaj7hom8a-6>li:before{content:"\0025cf   "}.lst-kix_xuggaj7hom8a-1>li:before{content:"\0025cb   "}.lst-kix_xuggaj7hom8a-0>li:before{content:"\0025cf   "}.lst-kix_xuggaj7hom8a-7>li:before{content:"\0025cb   "}.lst-kix_xuggaj7hom8a-8>li:before{content:"\0025a0   "}.lst-kix_xuggaj7hom8a-2>li:before{content:"\0025a0   "}.lst-kix_xuggaj7hom8a-3>li:before{content:"\0025cf   "}.lst-kix_xuggaj7hom8a-4>li:before{content:"\0025cb   "}ul.lst-kix_b5kgyf18mwbc-3{list-style-type:none}ul.lst-kix_b5kgyf18mwbc-4{list-style-type:none}ul.lst-kix_b5kgyf18mwbc-5{list-style-type:none}ul.lst-kix_b5kgyf18mwbc-6{list-style-type:none}ul.lst-kix_b5kgyf18mwbc-7{list-style-type:none}ul.lst-kix_b5kgyf18mwbc-8{list-style-type:none}.lst-kix_o4sb2cmvbb1n-4>li:before{content:"\0025cb   "}ul.lst-kix_b5kgyf18mwbc-0{list-style-type:none}ul.lst-kix_b5kgyf18mwbc-1{list-style-type:none}ul.lst-kix_b5kgyf18mwbc-2{list-style-type:none}.lst-kix_o4sb2cmvbb1n-0>li:before{content:"\0025cf   "}.lst-kix_o4sb2cmvbb1n-2>li:before{content:"\0025a0   "}ol.lst-kix_g6xizdwyjqq3-1.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-1 0}.lst-kix_flhk8lcnzp86-0>li:before{content:"\0025cf   "}.lst-kix_flhk8lcnzp86-4>li:before{content:"\0025cb   "}.lst-kix_3xsvf8xpqkr-0>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-0}.lst-kix_oox587co29ny-5>li:before{content:"\0025a0   "}ul.lst-kix_flhk8lcnzp86-1{list-style-type:none}ul.lst-kix_flhk8lcnzp86-2{list-style-type:none}.lst-kix_o4sb2cmvbb1n-6>li:before{content:"\0025cf   "}ul.lst-kix_flhk8lcnzp86-3{list-style-type:none}ul.lst-kix_flhk8lcnzp86-4{list-style-type:none}.lst-kix_oox587co29ny-3>li:before{content:"\0025cf   "}ul.lst-kix_flhk8lcnzp86-0{list-style-type:none}.lst-kix_oox587co29ny-1>li:before{content:"\0025cb   "}.lst-kix_o4sb2cmvbb1n-8>li:before{content:"\0025a0   "}.lst-kix_flhk8lcnzp86-2>li:before{content:"\0025a0   "}.lst-kix_cfy6hfjc7ksl-0>li:before{content:"\0025cf   "}.lst-kix_aqyufb51wiu2-0>li:before{content:"\0025cf   "}.lst-kix_r38jvyodkvi3-6>li:before{content:"\0025cf   "}.lst-kix_7cx3ikmkibcd-8>li:before{content:"\0025a0   "}.lst-kix_cfy6hfjc7ksl-2>li:before{content:"\0025a0   "}.lst-kix_ow62cky4wecx-4>li:before{content:"\0025cb   "}.lst-kix_aqyufb51wiu2-2>li:before{content:"\0025a0   "}.lst-kix_r38jvyodkvi3-8>li:before{content:"\0025a0   "}.lst-kix_ow62cky4wecx-2>li:before{content:"\0025a0   "}.lst-kix_7cx3ikmkibcd-2>li:before{content:"\0025a0   "}.lst-kix_7cx3ikmkibcd-4>li:before{content:"\0025cb   "}.lst-kix_flhk8lcnzp86-6>li:before{content:"\0025cf   "}.lst-kix_flhk8lcnzp86-8>li:before{content:"\0025a0   "}.lst-kix_oox587co29ny-7>li:before{content:"\0025cb   "}.lst-kix_aqyufb51wiu2-4>li:before{content:"\0025cb   "}.lst-kix_aqyufb51wiu2-8>li:before{content:"\0025a0   "}.lst-kix_r38jvyodkvi3-2>li:before{content:"\0025a0   "}.lst-kix_7cx3ikmkibcd-6>li:before{content:"\0025cf   "}.lst-kix_ow62cky4wecx-0>li:before{content:"\0025cf   "}.lst-kix_aqyufb51wiu2-6>li:before{content:"\0025cf   "}.lst-kix_r38jvyodkvi3-4>li:before{content:"\0025cb   "}.lst-kix_7cx3ikmkibcd-0>li:before{content:"\0025cf   "}.lst-kix_cfy6hfjc7ksl-8>li:before{content:"\0025a0   "}ol.lst-kix_3xsvf8xpqkr-2.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-2 0}.lst-kix_cfy6hfjc7ksl-4>li:before{content:"\0025cb   "}.lst-kix_ow62cky4wecx-6>li:before{content:"\0025cf   "}.lst-kix_cfy6hfjc7ksl-6>li:before{content:"\0025cf   "}.lst-kix_ow62cky4wecx-8>li:before{content:"\0025a0   "}.lst-kix_aqvmchp8hu99-5>li:before{content:"\0025a0   "}.lst-kix_i9nqtalub2ii-7>li:before{content:"\0025cb   "}.lst-kix_i9nqtalub2ii-4>li:before{content:"\0025cb   "}.lst-kix_i9nqtalub2ii-8>li:before{content:"\0025a0   "}.lst-kix_aqvmchp8hu99-4>li:before{content:"\0025cb   "}.lst-kix_aqvmchp8hu99-8>li:before{content:"\0025a0   "}.lst-kix_3xsvf8xpqkr-7>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-7}.lst-kix_i9nqtalub2ii-3>li:before{content:"\0025cf   "}.lst-kix_ws5to0ylpjnu-2>li:before{content:"\0025a0   "}.lst-kix_o1xshf1f7b14-3>li:before{content:"\0025cf   "}.lst-kix_ws5to0ylpjnu-3>li:before{content:"\0025cf   "}.lst-kix_aqvmchp8hu99-0>li:before{content:"\0025cf   "}.lst-kix_o1xshf1f7b14-7>li:before{content:"\0025cb   "}.lst-kix_aqvmchp8hu99-1>li:before{content:"\0025cb   "}.lst-kix_ws5to0ylpjnu-7>li:before{content:"\0025cb   "}.lst-kix_ws5to0ylpjnu-6>li:before{content:"\0025cf   "}.lst-kix_o1xshf1f7b14-6>li:before{content:"\0025cf   "}ul.lst-kix_mh8zxn2yduhi-0{list-style-type:none}.lst-kix_urbfmzpl5otu-2>li:before{content:"\0025a0   "}ul.lst-kix_mh8zxn2yduhi-3{list-style-type:none}ul.lst-kix_mh8zxn2yduhi-4{list-style-type:none}ul.lst-kix_mh8zxn2yduhi-1{list-style-type:none}ul.lst-kix_mh8zxn2yduhi-2{list-style-type:none}.lst-kix_urbfmzpl5otu-1>li:before{content:"\0025cb   "}.lst-kix_urbfmzpl5otu-5>li:before{content:"\0025a0   "}ol.lst-kix_3xsvf8xpqkr-3.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-3 0}ul.lst-kix_mh8zxn2yduhi-7{list-style-type:none}ul.lst-kix_mh8zxn2yduhi-8{list-style-type:none}ul.lst-kix_mh8zxn2yduhi-5{list-style-type:none}ul.lst-kix_mh8zxn2yduhi-6{list-style-type:none}ul.lst-kix_v6l0cypl4mld-0{list-style-type:none}ul.lst-kix_v6l0cypl4mld-1{list-style-type:none}.lst-kix_oblnvdf1x5se-0>li:before{content:"\0025cf   "}.lst-kix_vjixo3ysi0xu-8>li:before{content:"\0025a0   "}.lst-kix_t3aqzvl38zqp-0>li:before{content:"\0025cf   "}.lst-kix_oblnvdf1x5se-3>li:before{content:"\0025cf   "}ul.lst-kix_v6l0cypl4mld-6{list-style-type:none}ul.lst-kix_v6l0cypl4mld-7{list-style-type:none}ul.lst-kix_v6l0cypl4mld-8{list-style-type:none}.lst-kix_vjixo3ysi0xu-7>li:before{content:"\0025cb   "}.lst-kix_oblnvdf1x5se-4>li:before{content:"\0025cb   "}ul.lst-kix_v6l0cypl4mld-2{list-style-type:none}.lst-kix_t3aqzvl38zqp-1>li:before{content:"\0025cb   "}ul.lst-kix_flhk8lcnzp86-5{list-style-type:none}ul.lst-kix_v6l0cypl4mld-3{list-style-type:none}ul.lst-kix_flhk8lcnzp86-6{list-style-type:none}ul.lst-kix_v6l0cypl4mld-4{list-style-type:none}ul.lst-kix_flhk8lcnzp86-7{list-style-type:none}ul.lst-kix_v6l0cypl4mld-5{list-style-type:none}ul.lst-kix_flhk8lcnzp86-8{list-style-type:none}.lst-kix_vjixo3ysi0xu-3>li:before{content:"\0025cf   "}.lst-kix_vjixo3ysi0xu-0>li:before{content:"\0025cf   "}.lst-kix_vjixo3ysi0xu-4>li:before{content:"\0025cb   "}ol.lst-kix_g6xizdwyjqq3-6.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-6 0}.lst-kix_t3aqzvl38zqp-4>li:before{content:"\0025cb   "}.lst-kix_t3aqzvl38zqp-8>li:before{content:"\0025a0   "}.lst-kix_urbfmzpl5otu-6>li:before{content:"\0025cf   "}.lst-kix_t3aqzvl38zqp-5>li:before{content:"\0025a0   "}.lst-kix_nm8cz258lm3y-3>li:before{content:"\0025cf   "}.lst-kix_nm8cz258lm3y-2>li:before{content:"\0025a0   "}.lst-kix_nm8cz258lm3y-7>li:before{content:"\0025cb   "}.lst-kix_o1xshf1f7b14-2>li:before{content:"\0025a0   "}.lst-kix_nm8cz258lm3y-6>li:before{content:"\0025cf   "}.lst-kix_oblnvdf1x5se-7>li:before{content:"\0025cb   "}ol.lst-kix_g6xizdwyjqq3-5.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-5 0}.lst-kix_oblnvdf1x5se-8>li:before{content:"\0025a0   "}.lst-kix_i9nqtalub2ii-0>li:before{content:"\0025cf   "}.lst-kix_pa8vl4tnpl8x-1>li:before{content:"\0025cb   "}.lst-kix_q0ktwdf5md65-0>li:before{content:"\0025cf   "}.lst-kix_pa8vl4tnpl8x-5>li:before{content:"\0025a0   "}.lst-kix_8163nc3u15jq-8>li:before{content:"\0025a0   "}.lst-kix_o4sb2cmvbb1n-3>li:before{content:"\0025cf   "}.lst-kix_q0ktwdf5md65-4>li:before{content:"\0025cb   "}ul.lst-kix_kfoqz7rveyph-8{list-style-type:none}ul.lst-kix_kfoqz7rveyph-7{list-style-type:none}.lst-kix_8163nc3u15jq-0>li:before{content:"\0025cf   "}.lst-kix_8163nc3u15jq-4>li:before{content:"\0025cb   "}.lst-kix_o4sb2cmvbb1n-7>li:before{content:"\0025cb   "}ol.lst-kix_3xsvf8xpqkr-7.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-7 0}ul.lst-kix_kfoqz7rveyph-0{list-style-type:none}.lst-kix_flhk8lcnzp86-3>li:before{content:"\0025cf   "}ul.lst-kix_kfoqz7rveyph-2{list-style-type:none}.lst-kix_oox587co29ny-2>li:before{content:"\0025a0   "}ul.lst-kix_kfoqz7rveyph-1{list-style-type:none}ul.lst-kix_kfoqz7rveyph-4{list-style-type:none}ul.lst-kix_kfoqz7rveyph-3{list-style-type:none}ul.lst-kix_kfoqz7rveyph-6{list-style-type:none}ul.lst-kix_kfoqz7rveyph-5{list-style-type:none}.lst-kix_72e2zqulhrwf-1>li:before{content:"\0025cb   "}.lst-kix_aqyufb51wiu2-1>li:before{content:"\0025cb   "}.lst-kix_cfy6hfjc7ksl-1>li:before{content:"\0025cb   "}.lst-kix_g6xizdwyjqq3-4>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-4}.lst-kix_ow62cky4wecx-3>li:before{content:"\0025cf   "}.lst-kix_72e2zqulhrwf-5>li:before{content:"\0025a0   "}.lst-kix_r38jvyodkvi3-1>li:before{content:"\0025cb   "}.lst-kix_flhk8lcnzp86-7>li:before{content:"\0025cb   "}.lst-kix_oox587co29ny-6>li:before{content:"\0025cf   "}.lst-kix_r38jvyodkvi3-5>li:before{content:"\0025a0   "}.lst-kix_aqyufb51wiu2-5>li:before{content:"\0025a0   "}.lst-kix_7cx3ikmkibcd-5>li:before{content:"\0025a0   "}.lst-kix_3xsvf8xpqkr-2>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-2}.lst-kix_7cx3ikmkibcd-1>li:before{content:"\0025cb   "}ol.lst-kix_3xsvf8xpqkr-8.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-8 0}ul.lst-kix_dceblroryw8x-1{list-style-type:none}ul.lst-kix_dceblroryw8x-0{list-style-type:none}ul.lst-kix_dceblroryw8x-3{list-style-type:none}ul.lst-kix_dceblroryw8x-2{list-style-type:none}.lst-kix_q0ktwdf5md65-8>li:before{content:"\0025a0   "}ul.lst-kix_dceblroryw8x-5{list-style-type:none}ul.lst-kix_dceblroryw8x-4{list-style-type:none}ul.lst-kix_dceblroryw8x-7{list-style-type:none}ul.lst-kix_dceblroryw8x-6{list-style-type:none}ul.lst-kix_dceblroryw8x-8{list-style-type:none}.lst-kix_cfy6hfjc7ksl-5>li:before{content:"\0025a0   "}.lst-kix_ow62cky4wecx-7>li:before{content:"\0025cb   "}.lst-kix_g6xizdwyjqq3-6>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-6}.lst-kix_6cl8b4hxtxv-7>li:before{content:"\0025cb   "}.lst-kix_3xsvf8xpqkr-6>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-6}ul.lst-kix_o1xshf1f7b14-1{list-style-type:none}ul.lst-kix_o1xshf1f7b14-2{list-style-type:none}ul.lst-kix_o1xshf1f7b14-0{list-style-type:none}ul.lst-kix_o1xshf1f7b14-7{list-style-type:none}ul.lst-kix_o1xshf1f7b14-8{list-style-type:none}ul.lst-kix_o1xshf1f7b14-5{list-style-type:none}ul.lst-kix_o1xshf1f7b14-6{list-style-type:none}ul.lst-kix_o1xshf1f7b14-3{list-style-type:none}ul.lst-kix_o1xshf1f7b14-4{list-style-type:none}.lst-kix_yztclpytevvw-7>li:before{content:"\0025cb   "}.lst-kix_lrkiroe9ekhf-5>li:before{content:"\0025a0   "}.lst-kix_6cl8b4hxtxv-1>li:before{content:"\0025cb   "}.lst-kix_6cl8b4hxtxv-2>li:before{content:"\0025a0   "}.lst-kix_yztclpytevvw-2>li:before{content:"\0025a0   "}.lst-kix_yztclpytevvw-4>li:before{content:"\0025cb   "}.lst-kix_lrkiroe9ekhf-7>li:before{content:"\0025cb   "}ol.lst-kix_3xsvf8xpqkr-6.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-6 0}.lst-kix_yztclpytevvw-5>li:before{content:"\0025a0   "}.lst-kix_6cl8b4hxtxv-4>li:before{content:"\0025cb   "}.lst-kix_lrkiroe9ekhf-2>li:before{content:"\0025a0   "}.lst-kix_lrkiroe9ekhf-4>li:before{content:"\0025cb   "}.lst-kix_pa8vl4tnpl8x-2>li:before{content:"\0025a0   "}ol.lst-kix_3xsvf8xpqkr-4.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-4 0}.lst-kix_pa8vl4tnpl8x-4>li:before{content:"\0025cb   "}ul.lst-kix_t3aqzvl38zqp-8{list-style-type:none}ul.lst-kix_t3aqzvl38zqp-7{list-style-type:none}ul.lst-kix_t3aqzvl38zqp-6{list-style-type:none}ul.lst-kix_t3aqzvl38zqp-5{list-style-type:none}ul.lst-kix_t3aqzvl38zqp-4{list-style-type:none}ul.lst-kix_t3aqzvl38zqp-3{list-style-type:none}ul.lst-kix_t3aqzvl38zqp-2{list-style-type:none}ul.lst-kix_t3aqzvl38zqp-1{list-style-type:none}.lst-kix_3xsvf8xpqkr-6>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-6,decimal) ". "}ul.lst-kix_t3aqzvl38zqp-0{list-style-type:none}.lst-kix_8163nc3u15jq-7>li:before{content:"\0025cb   "}.lst-kix_q0ktwdf5md65-5>li:before{content:"\0025a0   "}.lst-kix_chmeg86wx98z-4>li:before{content:"\0025cb   "}.lst-kix_chmeg86wx98z-2>li:before{content:"\0025a0   "}ol.lst-kix_g6xizdwyjqq3-4.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-4 0}.lst-kix_3xsvf8xpqkr-0>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-0,decimal) ". "}ol.lst-kix_3xsvf8xpqkr-1.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-1 0}ul.lst-kix_hy2j2rjtl7zm-8{list-style-type:none}ul.lst-kix_8163nc3u15jq-0{list-style-type:none}ul.lst-kix_hy2j2rjtl7zm-1{list-style-type:none}ul.lst-kix_8163nc3u15jq-6{list-style-type:none}ul.lst-kix_hy2j2rjtl7zm-0{list-style-type:none}ul.lst-kix_8163nc3u15jq-5{list-style-type:none}ul.lst-kix_hy2j2rjtl7zm-3{list-style-type:none}ul.lst-kix_8163nc3u15jq-8{list-style-type:none}ul.lst-kix_nm8cz258lm3y-0{list-style-type:none}ul.lst-kix_hy2j2rjtl7zm-2{list-style-type:none}ul.lst-kix_8163nc3u15jq-7{list-style-type:none}ul.lst-kix_hy2j2rjtl7zm-5{list-style-type:none}ul.lst-kix_8163nc3u15jq-2{list-style-type:none}ul.lst-kix_nm8cz258lm3y-2{list-style-type:none}ul.lst-kix_hy2j2rjtl7zm-4{list-style-type:none}ul.lst-kix_8163nc3u15jq-1{list-style-type:none}ul.lst-kix_nm8cz258lm3y-1{list-style-type:none}ul.lst-kix_hy2j2rjtl7zm-7{list-style-type:none}ul.lst-kix_8163nc3u15jq-4{list-style-type:none}ul.lst-kix_nm8cz258lm3y-4{list-style-type:none}ul.lst-kix_hy2j2rjtl7zm-6{list-style-type:none}ul.lst-kix_8163nc3u15jq-3{list-style-type:none}ul.lst-kix_nm8cz258lm3y-3{list-style-type:none}ul.lst-kix_nm8cz258lm3y-6{list-style-type:none}ul.lst-kix_nm8cz258lm3y-5{list-style-type:none}ul.lst-kix_nm8cz258lm3y-8{list-style-type:none}ul.lst-kix_nm8cz258lm3y-7{list-style-type:none}.lst-kix_8163nc3u15jq-5>li:before{content:"\0025a0   "}ol.lst-kix_g6xizdwyjqq3-2.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-2 0}.lst-kix_72e2zqulhrwf-2>li:before{content:"\0025a0   "}.lst-kix_72e2zqulhrwf-4>li:before{content:"\0025cb   "}.lst-kix_28qbb5pba8ll-0>li:before{content:"\0025cf   "}.lst-kix_4xenxtb85rpl-3>li:before{content:"\0025cf   "}.lst-kix_28qbb5pba8ll-2>li:before{content:"\0025a0   "}ul.lst-kix_pa8vl4tnpl8x-4{list-style-type:none}ul.lst-kix_pa8vl4tnpl8x-5{list-style-type:none}ul.lst-kix_pa8vl4tnpl8x-6{list-style-type:none}ul.lst-kix_pa8vl4tnpl8x-7{list-style-type:none}ul.lst-kix_pa8vl4tnpl8x-8{list-style-type:none}ul.lst-kix_pa8vl4tnpl8x-0{list-style-type:none}ul.lst-kix_pa8vl4tnpl8x-1{list-style-type:none}.lst-kix_q0ktwdf5md65-7>li:before{content:"\0025cb   "}ul.lst-kix_pa8vl4tnpl8x-2{list-style-type:none}ul.lst-kix_pa8vl4tnpl8x-3{list-style-type:none}.lst-kix_4xenxtb85rpl-5>li:before{content:"\0025a0   "}.lst-kix_3xsvf8xpqkr-8>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-8,lower-roman) ". "}.lst-kix_28qbb5pba8ll-8>li:before{content:"\0025a0   "}.lst-kix_i9nqtalub2ii-5>li:before{content:"\0025a0   "}.lst-kix_aqvmchp8hu99-7>li:before{content:"\0025cb   "}.lst-kix_o1xshf1f7b14-8>li:before{content:"\0025a0   "}.lst-kix_lenutxuehbqs-7>li:before{content:"\0025cb   "}.lst-kix_i9nqtalub2ii-2>li:before{content:"\0025a0   "}.lst-kix_ws5to0ylpjnu-0>li:before{content:"\0025cf   "}ul.lst-kix_oblnvdf1x5se-8{list-style-type:none}ul.lst-kix_oblnvdf1x5se-6{list-style-type:none}ul.lst-kix_oblnvdf1x5se-7{list-style-type:none}ul.lst-kix_oblnvdf1x5se-4{list-style-type:none}ul.lst-kix_ws5to0ylpjnu-0{list-style-type:none}ul.lst-kix_oblnvdf1x5se-5{list-style-type:none}ul.lst-kix_ws5to0ylpjnu-2{list-style-type:none}.lst-kix_wwfczwp99rcu-4>li:before{content:"\0025cb   "}ul.lst-kix_ws5to0ylpjnu-1{list-style-type:none}ul.lst-kix_ws5to0ylpjnu-4{list-style-type:none}ul.lst-kix_ws5to0ylpjnu-3{list-style-type:none}.lst-kix_o1xshf1f7b14-5>li:before{content:"\0025a0   "}ul.lst-kix_ws5to0ylpjnu-6{list-style-type:none}ul.lst-kix_ws5to0ylpjnu-5{list-style-type:none}ul.lst-kix_ws5to0ylpjnu-8{list-style-type:none}ul.lst-kix_ws5to0ylpjnu-7{list-style-type:none}.lst-kix_slhmqripkczd-7>li:before{content:"\0025cb   "}.lst-kix_dceblroryw8x-8>li:before{content:"\0025a0   "}.lst-kix_ws5to0ylpjnu-5>li:before{content:"\0025a0   "}.lst-kix_insf2ook9lmq-8>li:before{content:"\0025a0   "}.lst-kix_aqvmchp8hu99-2>li:before{content:"\0025a0   "}.lst-kix_nm8cz258lm3y-1>li:before{content:"\0025cb   "}.lst-kix_rzwdtfa96ijp-2>li:before{content:"\0025a0   "}.lst-kix_urbfmzpl5otu-4>li:before{content:"\0025cb   "}.lst-kix_hy2j2rjtl7zm-3>li:before{content:"\0025cf   "}.lst-kix_lenutxuehbqs-4>li:before{content:"\0025cb   "}.lst-kix_hy2j2rjtl7zm-6>li:before{content:"\0025cf   "}.lst-kix_wwfczwp99rcu-1>li:before{content:"\0025cb   "}.lst-kix_rzwdtfa96ijp-7>li:before{content:"\0025cb   "}ol.lst-kix_g6xizdwyjqq3-0.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-0 0}.lst-kix_b5kgyf18mwbc-2>li:before{content:"\0025a0   "}ul.lst-kix_wwfczwp99rcu-0{list-style-type:none}ul.lst-kix_wwfczwp99rcu-2{list-style-type:none}ul.lst-kix_wwfczwp99rcu-1{list-style-type:none}.lst-kix_b5kgyf18mwbc-5>li:before{content:"\0025a0   "}.lst-kix_t3aqzvl38zqp-3>li:before{content:"\0025cf   "}.lst-kix_vjixo3ysi0xu-5>li:before{content:"\0025a0   "}.lst-kix_vjixo3ysi0xu-2>li:before{content:"\0025a0   "}.lst-kix_v6l0cypl4mld-6>li:before{content:"\0025cf   "}ul.lst-kix_wwfczwp99rcu-4{list-style-type:none}ul.lst-kix_wwfczwp99rcu-3{list-style-type:none}ul.lst-kix_wwfczwp99rcu-6{list-style-type:none}ul.lst-kix_wwfczwp99rcu-5{list-style-type:none}ul.lst-kix_wwfczwp99rcu-8{list-style-type:none}ul.lst-kix_wwfczwp99rcu-7{list-style-type:none}.lst-kix_t3aqzvl38zqp-6>li:before{content:"\0025cf   "}.lst-kix_oblnvdf1x5se-1>li:before{content:"\0025cb   "}.lst-kix_urbfmzpl5otu-7>li:before{content:"\0025cb   "}.lst-kix_dceblroryw8x-5>li:before{content:"\0025a0   "}.lst-kix_7n6k9dq04clh-7>li:before{content:"\0025cb   "}.lst-kix_nm8cz258lm3y-4>li:before{content:"\0025cb   "}.lst-kix_chmeg86wx98z-7>li:before{content:"\0025cb   "}ul.lst-kix_oblnvdf1x5se-2{list-style-type:none}ul.lst-kix_oblnvdf1x5se-3{list-style-type:none}ul.lst-kix_oblnvdf1x5se-0{list-style-type:none}ul.lst-kix_oblnvdf1x5se-1{list-style-type:none}.lst-kix_oblnvdf1x5se-6>li:before{content:"\0025cf   "}.lst-kix_o1xshf1f7b14-0>li:before{content:"\0025cf   "}.lst-kix_dceblroryw8x-0>li:before{content:"\0025cf   "}.lst-kix_7n6k9dq04clh-2>li:before{content:"\0025a0   "}.lst-kix_3xsvf8xpqkr-3>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-3,decimal) ". "}.lst-kix_pa8vl4tnpl8x-7>li:before{content:"\0025cb   "}.lst-kix_fhmjbje0v4d4-7>li:before{content:"\0025cb   "}.lst-kix_o4sb2cmvbb1n-1>li:before{content:"\0025cb   "}.lst-kix_q0ktwdf5md65-2>li:before{content:"\0025a0   "}ul.lst-kix_urbfmzpl5otu-1{list-style-type:none}.lst-kix_v6l0cypl4mld-3>li:before{content:"\0025cf   "}ul.lst-kix_urbfmzpl5otu-0{list-style-type:none}ul.lst-kix_urbfmzpl5otu-3{list-style-type:none}ul.lst-kix_urbfmzpl5otu-2{list-style-type:none}ul.lst-kix_urbfmzpl5otu-5{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-2{list-style-type:none}ul.lst-kix_urbfmzpl5otu-4{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-3{list-style-type:none}ul.lst-kix_urbfmzpl5otu-7{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-4{list-style-type:none}ul.lst-kix_urbfmzpl5otu-6{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-5{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-6{list-style-type:none}.lst-kix_flhk8lcnzp86-5>li:before{content:"\0025a0   "}ul.lst-kix_urbfmzpl5otu-8{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-7{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-8{list-style-type:none}.lst-kix_3xsvf8xpqkr-3>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-3}ol.lst-kix_g6xizdwyjqq3-0{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-1{list-style-type:none}.lst-kix_mh8zxn2yduhi-4>li:before{content:"\0025cb   "}.lst-kix_8163nc3u15jq-2>li:before{content:"\0025a0   "}.lst-kix_oox587co29ny-0>li:before{content:"\0025cf   "}ul.lst-kix_4xenxtb85rpl-7{list-style-type:none}ul.lst-kix_4xenxtb85rpl-8{list-style-type:none}ul.lst-kix_4xenxtb85rpl-5{list-style-type:none}ul.lst-kix_4xenxtb85rpl-6{list-style-type:none}.lst-kix_r38jvyodkvi3-7>li:before{content:"\0025cb   "}ul.lst-kix_4xenxtb85rpl-3{list-style-type:none}ul.lst-kix_4xenxtb85rpl-4{list-style-type:none}ul.lst-kix_4xenxtb85rpl-1{list-style-type:none}ul.lst-kix_4xenxtb85rpl-2{list-style-type:none}.lst-kix_aqyufb51wiu2-3>li:before{content:"\0025cf   "}ul.lst-kix_4xenxtb85rpl-0{list-style-type:none}.lst-kix_cfy6hfjc7ksl-3>li:before{content:"\0025cf   "}.lst-kix_7cx3ikmkibcd-3>li:before{content:"\0025cf   "}.lst-kix_ow62cky4wecx-1>li:before{content:"\0025cb   "}.lst-kix_g6xizdwyjqq3-3>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-3}.lst-kix_oox587co29ny-8>li:before{content:"\0025a0   "}.lst-kix_72e2zqulhrwf-7>li:before{content:"\0025cb   "}.lst-kix_28qbb5pba8ll-5>li:before{content:"\0025a0   "}.lst-kix_slhmqripkczd-4>li:before{content:"\0025cb   "}.lst-kix_insf2ook9lmq-5>li:before{content:"\0025a0   "}.lst-kix_ws5to0ylpjnu-8>li:before{content:"\0025a0   "}li.li-bullet-0:before{margin-left:-18pt;white-space:nowrap;display:inline-block;min-width:18pt}.lst-kix_4xenxtb85rpl-0>li:before{content:"\0025cf   "}.lst-kix_4xenxtb85rpl-8>li:before{content:"\0025a0   "}.lst-kix_dwl4sw54czlu-2>li:before{content:"\0025a0   "}ul.lst-kix_vjixo3ysi0xu-7{list-style-type:none}ul.lst-kix_vjixo3ysi0xu-6{list-style-type:none}.lst-kix_dwl4sw54czlu-1>li:before{content:"\0025cb   "}.lst-kix_dwl4sw54czlu-3>li:before{content:"\0025cf   "}ul.lst-kix_vjixo3ysi0xu-5{list-style-type:none}ul.lst-kix_vjixo3ysi0xu-4{list-style-type:none}.lst-kix_dwl4sw54czlu-0>li:before{content:"\0025cf   "}.lst-kix_dwl4sw54czlu-4>li:before{content:"\0025cb   "}ul.lst-kix_vjixo3ysi0xu-8{list-style-type:none}.lst-kix_dwl4sw54czlu-6>li:before{content:"\0025cf   "}.lst-kix_dwl4sw54czlu-5>li:before{content:"\0025a0   "}ul.lst-kix_vjixo3ysi0xu-3{list-style-type:none}ul.lst-kix_vjixo3ysi0xu-2{list-style-type:none}ul.lst-kix_vjixo3ysi0xu-1{list-style-type:none}ul.lst-kix_vjixo3ysi0xu-0{list-style-type:none}.lst-kix_l255a4vu3t0u-6>li:before{content:"\0025cf   "}.lst-kix_l255a4vu3t0u-5>li:before{content:"\0025a0   "}.lst-kix_l255a4vu3t0u-7>li:before{content:"\0025cb   "}ul.lst-kix_q0ktwdf5md65-7{list-style-type:none}ul.lst-kix_q0ktwdf5md65-8{list-style-type:none}.lst-kix_l255a4vu3t0u-8>li:before{content:"\0025a0   "}.lst-kix_l255a4vu3t0u-2>li:before{content:"\0025a0   "}ol.lst-kix_3xsvf8xpqkr-0.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-0 0}ul.lst-kix_q0ktwdf5md65-3{list-style-type:none}ul.lst-kix_ow62cky4wecx-7{list-style-type:none}ul.lst-kix_q0ktwdf5md65-4{list-style-type:none}ul.lst-kix_ow62cky4wecx-8{list-style-type:none}ul.lst-kix_q0ktwdf5md65-5{list-style-type:none}ul.lst-kix_q0ktwdf5md65-6{list-style-type:none}.lst-kix_l255a4vu3t0u-3>li:before{content:"\0025cf   "}ul.lst-kix_q0ktwdf5md65-0{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-3.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-3 0}ul.lst-kix_q0ktwdf5md65-1{list-style-type:none}ul.lst-kix_q0ktwdf5md65-2{list-style-type:none}.lst-kix_l255a4vu3t0u-4>li:before{content:"\0025cb   "}ul.lst-kix_ow62cky4wecx-0{list-style-type:none}ul.lst-kix_ow62cky4wecx-1{list-style-type:none}ul.lst-kix_ow62cky4wecx-2{list-style-type:none}ul.lst-kix_ow62cky4wecx-3{list-style-type:none}.lst-kix_dwl4sw54czlu-7>li:before{content:"\0025cb   "}.lst-kix_dwl4sw54czlu-8>li:before{content:"\0025a0   "}ul.lst-kix_ow62cky4wecx-4{list-style-type:none}ul.lst-kix_ow62cky4wecx-5{list-style-type:none}ul.lst-kix_ow62cky4wecx-6{list-style-type:none}.lst-kix_l255a4vu3t0u-1>li:before{content:"\0025cb   "}.lst-kix_l255a4vu3t0u-0>li:before{content:"\0025cf   "}.lst-kix_3xsvf8xpqkr-4>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-4}ul.lst-kix_aqvmchp8hu99-8{list-style-type:none}.lst-kix_kfoqz7rveyph-6>li:before{content:"\0025cf   "}.lst-kix_kfoqz7rveyph-7>li:before{content:"\0025cb   "}.lst-kix_kfoqz7rveyph-8>li:before{content:"\0025a0   "}ul.lst-kix_aqvmchp8hu99-1{list-style-type:none}ul.lst-kix_aqvmchp8hu99-0{list-style-type:none}ul.lst-kix_aqvmchp8hu99-3{list-style-type:none}ul.lst-kix_aqvmchp8hu99-2{list-style-type:none}ul.lst-kix_aqvmchp8hu99-5{list-style-type:none}ul.lst-kix_aqvmchp8hu99-4{list-style-type:none}ul.lst-kix_aqvmchp8hu99-7{list-style-type:none}ul.lst-kix_aqvmchp8hu99-6{list-style-type:none}ol.lst-kix_3xsvf8xpqkr-5.start{counter-reset:lst-ctn-kix_3xsvf8xpqkr-5 0}.lst-kix_kfoqz7rveyph-5>li:before{content:"\0025a0   "}.lst-kix_kfoqz7rveyph-4>li:before{content:"\0025cb   "}.lst-kix_kfoqz7rveyph-2>li:before{content:"\0025a0   "}.lst-kix_kfoqz7rveyph-3>li:before{content:"\0025cf   "}.lst-kix_kfoqz7rveyph-0>li:before{content:"\0025cf   "}.lst-kix_g6xizdwyjqq3-8>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-8}.lst-kix_kfoqz7rveyph-1>li:before{content:"\0025cb   "}.lst-kix_mh8zxn2yduhi-7>li:before{content:"\0025cb   "}.lst-kix_fhmjbje0v4d4-4>li:before{content:"\0025cb   "}.lst-kix_fhmjbje0v4d4-8>li:before{content:"\0025a0   "}.lst-kix_mh8zxn2yduhi-3>li:before{content:"\0025cf   "}.lst-kix_g6xizdwyjqq3-1>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-1}.lst-kix_fhmjbje0v4d4-6>li:before{content:"\0025cf   "}.lst-kix_mh8zxn2yduhi-1>li:before{content:"\0025cb   "}.lst-kix_fhmjbje0v4d4-0>li:before{content:"\0025cf   "}.lst-kix_fhmjbje0v4d4-2>li:before{content:"\0025a0   "}.lst-kix_g6xizdwyjqq3-0>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-0}.lst-kix_v6l0cypl4mld-0>li:before{content:"\0025cf   "}.lst-kix_v6l0cypl4mld-2>li:before{content:"\0025a0   "}ul.lst-kix_r38jvyodkvi3-7{list-style-type:none}ul.lst-kix_r38jvyodkvi3-8{list-style-type:none}ul.lst-kix_r38jvyodkvi3-5{list-style-type:none}ul.lst-kix_r38jvyodkvi3-6{list-style-type:none}ul.lst-kix_r38jvyodkvi3-3{list-style-type:none}ul.lst-kix_r38jvyodkvi3-4{list-style-type:none}ul.lst-kix_r38jvyodkvi3-1{list-style-type:none}ul.lst-kix_slhmqripkczd-0{list-style-type:none}ul.lst-kix_r38jvyodkvi3-2{list-style-type:none}ul.lst-kix_slhmqripkczd-1{list-style-type:none}ul.lst-kix_slhmqripkczd-2{list-style-type:none}ul.lst-kix_slhmqripkczd-3{list-style-type:none}.lst-kix_mh8zxn2yduhi-5>li:before{content:"\0025a0   "}ul.lst-kix_slhmqripkczd-4{list-style-type:none}ul.lst-kix_slhmqripkczd-5{list-style-type:none}ul.lst-kix_slhmqripkczd-6{list-style-type:none}ul.lst-kix_slhmqripkczd-7{list-style-type:none}ul.lst-kix_slhmqripkczd-8{list-style-type:none}.lst-kix_b5kgyf18mwbc-1>li:before{content:"\0025cb   "}ul.lst-kix_r38jvyodkvi3-0{list-style-type:none}.lst-kix_slhmqripkczd-3>li:before{content:"\0025cf   "}.lst-kix_3xsvf8xpqkr-5>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-5}.lst-kix_insf2ook9lmq-6>li:before{content:"\0025cf   "}.lst-kix_slhmqripkczd-1>li:before{content:"\0025cb   "}.lst-kix_insf2ook9lmq-4>li:before{content:"\0025cb   "}.lst-kix_insf2ook9lmq-2>li:before{content:"\0025a0   "}.lst-kix_insf2ook9lmq-0>li:before{content:"\0025cf   "}ul.lst-kix_fhmjbje0v4d4-3{list-style-type:none}ul.lst-kix_fhmjbje0v4d4-4{list-style-type:none}ul.lst-kix_fhmjbje0v4d4-1{list-style-type:none}ul.lst-kix_fhmjbje0v4d4-2{list-style-type:none}ul.lst-kix_fhmjbje0v4d4-7{list-style-type:none}.lst-kix_wwfczwp99rcu-2>li:before{content:"\0025a0   "}ul.lst-kix_fhmjbje0v4d4-8{list-style-type:none}ul.lst-kix_fhmjbje0v4d4-5{list-style-type:none}ul.lst-kix_fhmjbje0v4d4-6{list-style-type:none}.lst-kix_wwfczwp99rcu-3>li:before{content:"\0025cf   "}ol.lst-kix_3xsvf8xpqkr-0{list-style-type:none}.lst-kix_g6xizdwyjqq3-7>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-7}ol.lst-kix_3xsvf8xpqkr-3{list-style-type:none}ol.lst-kix_3xsvf8xpqkr-4{list-style-type:none}ol.lst-kix_3xsvf8xpqkr-1{list-style-type:none}ol.lst-kix_3xsvf8xpqkr-2{list-style-type:none}ol.lst-kix_3xsvf8xpqkr-7{list-style-type:none}.lst-kix_wwfczwp99rcu-7>li:before{content:"\0025cb   "}ol.lst-kix_3xsvf8xpqkr-8{list-style-type:none}ol.lst-kix_3xsvf8xpqkr-5{list-style-type:none}.lst-kix_slhmqripkczd-6>li:before{content:"\0025cf   "}ol.lst-kix_3xsvf8xpqkr-6{list-style-type:none}.lst-kix_slhmqripkczd-5>li:before{content:"\0025a0   "}.lst-kix_wwfczwp99rcu-6>li:before{content:"\0025cf   "}.lst-kix_hy2j2rjtl7zm-0>li:before{content:"\0025cf   "}.lst-kix_hy2j2rjtl7zm-1>li:before{content:"\0025cb   "}.lst-kix_rzwdtfa96ijp-1>li:before{content:"\0025cb   "}.lst-kix_hy2j2rjtl7zm-4>li:before{content:"\0025cb   "}.lst-kix_hy2j2rjtl7zm-5>li:before{content:"\0025a0   "}.lst-kix_rzwdtfa96ijp-0>li:before{content:"\0025cf   "}.lst-kix_rzwdtfa96ijp-8>li:before{content:"\0025a0   "}.lst-kix_lenutxuehbqs-1>li:before{content:"\0025cb   "}.lst-kix_hy2j2rjtl7zm-8>li:before{content:"\0025a0   "}.lst-kix_lenutxuehbqs-2>li:before{content:"\0025a0   "}.lst-kix_rzwdtfa96ijp-5>li:before{content:"\0025a0   "}.lst-kix_lenutxuehbqs-6>li:before{content:"\0025cf   "}.lst-kix_rzwdtfa96ijp-4>li:before{content:"\0025cb   "}.lst-kix_lenutxuehbqs-5>li:before{content:"\0025a0   "}.lst-kix_b5kgyf18mwbc-3>li:before{content:"\0025cf   "}.lst-kix_b5kgyf18mwbc-4>li:before{content:"\0025cb   "}.lst-kix_b5kgyf18mwbc-8>li:before{content:"\0025a0   "}.lst-kix_b5kgyf18mwbc-7>li:before{content:"\0025cb   "}.lst-kix_v6l0cypl4mld-8>li:before{content:"\0025a0   "}.lst-kix_v6l0cypl4mld-4>li:before{content:"\0025cb   "}.lst-kix_v6l0cypl4mld-5>li:before{content:"\0025a0   "}.lst-kix_dceblroryw8x-6>li:before{content:"\0025cf   "}.lst-kix_7n6k9dq04clh-5>li:before{content:"\0025a0   "}.lst-kix_dceblroryw8x-3>li:before{content:"\0025cf   "}.lst-kix_dceblroryw8x-7>li:before{content:"\0025cb   "}.lst-kix_7n6k9dq04clh-4>li:before{content:"\0025cb   "}.lst-kix_7n6k9dq04clh-8>li:before{content:"\0025a0   "}.lst-kix_chmeg86wx98z-8>li:before{content:"\0025a0   "}ul.lst-kix_fhmjbje0v4d4-0{list-style-type:none}.lst-kix_7n6k9dq04clh-0>li:before{content:"\0025cf   "}.lst-kix_dceblroryw8x-2>li:before{content:"\0025a0   "}.lst-kix_7n6k9dq04clh-1>li:before{content:"\0025cb   "}.lst-kix_fhmjbje0v4d4-5>li:before{content:"\0025a0   "}ol.lst-kix_g6xizdwyjqq3-7.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-7 0}.lst-kix_mh8zxn2yduhi-2>li:before{content:"\0025a0   "}.lst-kix_3xsvf8xpqkr-5>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-5,lower-roman) ". "}.lst-kix_chmeg86wx98z-1>li:before{content:"\0025cb   "}.lst-kix_fhmjbje0v4d4-1>li:before{content:"\0025cb   "}.lst-kix_3xsvf8xpqkr-1>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-1,lower-latin) ". "}.lst-kix_chmeg86wx98z-5>li:before{content:"\0025a0   "}.lst-kix_v6l0cypl4mld-1>li:before{content:"\0025cb   "}.lst-kix_yztclpytevvw-1>li:before{content:"\0025cb   "}ul.lst-kix_i9nqtalub2ii-6{list-style-type:none}ul.lst-kix_i9nqtalub2ii-7{list-style-type:none}ul.lst-kix_i9nqtalub2ii-4{list-style-type:none}ul.lst-kix_i9nqtalub2ii-5{list-style-type:none}.lst-kix_mh8zxn2yduhi-6>li:before{content:"\0025cf   "}ul.lst-kix_i9nqtalub2ii-2{list-style-type:none}ul.lst-kix_i9nqtalub2ii-3{list-style-type:none}ul.lst-kix_i9nqtalub2ii-0{list-style-type:none}ul.lst-kix_i9nqtalub2ii-1{list-style-type:none}ul.lst-kix_i9nqtalub2ii-8{list-style-type:none}.lst-kix_b5kgyf18mwbc-0>li:before{content:"\0025cf   "}ul.lst-kix_6cl8b4hxtxv-6{list-style-type:none}ul.lst-kix_6cl8b4hxtxv-7{list-style-type:none}ul.lst-kix_6cl8b4hxtxv-8{list-style-type:none}ul.lst-kix_6cl8b4hxtxv-2{list-style-type:none}ul.lst-kix_6cl8b4hxtxv-3{list-style-type:none}ul.lst-kix_6cl8b4hxtxv-4{list-style-type:none}ul.lst-kix_6cl8b4hxtxv-5{list-style-type:none}ol.lst-kix_g6xizdwyjqq3-8.start{counter-reset:lst-ctn-kix_g6xizdwyjqq3-8 0}.lst-kix_slhmqripkczd-2>li:before{content:"\0025a0   "}.lst-kix_insf2ook9lmq-7>li:before{content:"\0025cb   "}.lst-kix_28qbb5pba8ll-3>li:before{content:"\0025cf   "}.lst-kix_28qbb5pba8ll-7>li:before{content:"\0025cb   "}.lst-kix_4xenxtb85rpl-2>li:before{content:"\0025a0   "}ul.lst-kix_6cl8b4hxtxv-0{list-style-type:none}ul.lst-kix_6cl8b4hxtxv-1{list-style-type:none}.lst-kix_insf2ook9lmq-3>li:before{content:"\0025cf   "}.lst-kix_4xenxtb85rpl-6>li:before{content:"\0025cf   "}ul.lst-kix_oox587co29ny-6{list-style-type:none}ul.lst-kix_oox587co29ny-5{list-style-type:none}ul.lst-kix_oox587co29ny-4{list-style-type:none}ul.lst-kix_oox587co29ny-3{list-style-type:none}ul.lst-kix_oox587co29ny-2{list-style-type:none}ul.lst-kix_oox587co29ny-1{list-style-type:none}ul.lst-kix_oox587co29ny-0{list-style-type:none}.lst-kix_6cl8b4hxtxv-8>li:before{content:"\0025a0   "}ul.lst-kix_yztclpytevvw-2{list-style-type:none}ul.lst-kix_yztclpytevvw-3{list-style-type:none}ul.lst-kix_yztclpytevvw-0{list-style-type:none}ul.lst-kix_yztclpytevvw-1{list-style-type:none}ul.lst-kix_yztclpytevvw-6{list-style-type:none}ul.lst-kix_yztclpytevvw-7{list-style-type:none}ul.lst-kix_yztclpytevvw-4{list-style-type:none}ul.lst-kix_yztclpytevvw-5{list-style-type:none}ul.lst-kix_dwl4sw54czlu-5{list-style-type:none}ul.lst-kix_dwl4sw54czlu-6{list-style-type:none}ul.lst-kix_dwl4sw54czlu-3{list-style-type:none}ul.lst-kix_yztclpytevvw-8{list-style-type:none}ul.lst-kix_dwl4sw54czlu-4{list-style-type:none}ul.lst-kix_dwl4sw54czlu-7{list-style-type:none}ul.lst-kix_dwl4sw54czlu-8{list-style-type:none}ul.lst-kix_lrkiroe9ekhf-8{list-style-type:none}ul.lst-kix_dwl4sw54czlu-1{list-style-type:none}ul.lst-kix_dwl4sw54czlu-2{list-style-type:none}ul.lst-kix_dwl4sw54czlu-0{list-style-type:none}.lst-kix_yztclpytevvw-8>li:before{content:"\0025a0   "}.lst-kix_lrkiroe9ekhf-6>li:before{content:"\0025cf   "}.lst-kix_6cl8b4hxtxv-0>li:before{content:"\0025cf   "}.lst-kix_yztclpytevvw-3>li:before{content:"\0025cf   "}.lst-kix_6cl8b4hxtxv-3>li:before{content:"\0025cf   "}ul.lst-kix_l255a4vu3t0u-0{list-style-type:none}ul.lst-kix_l255a4vu3t0u-1{list-style-type:none}ul.lst-kix_l255a4vu3t0u-2{list-style-type:none}.lst-kix_6cl8b4hxtxv-6>li:before{content:"\0025cf   "}.lst-kix_yztclpytevvw-6>li:before{content:"\0025cf   "}.lst-kix_lrkiroe9ekhf-8>li:before{content:"\0025a0   "}.lst-kix_6cl8b4hxtxv-5>li:before{content:"\0025a0   "}.lst-kix_g6xizdwyjqq3-2>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-2}ul.lst-kix_l255a4vu3t0u-3{list-style-type:none}ul.lst-kix_l255a4vu3t0u-4{list-style-type:none}ul.lst-kix_l255a4vu3t0u-5{list-style-type:none}ul.lst-kix_l255a4vu3t0u-6{list-style-type:none}ul.lst-kix_l255a4vu3t0u-7{list-style-type:none}ul.lst-kix_l255a4vu3t0u-8{list-style-type:none}.lst-kix_lrkiroe9ekhf-3>li:before{content:"\0025cf   "}ul.lst-kix_lrkiroe9ekhf-0{list-style-type:none}ul.lst-kix_lrkiroe9ekhf-1{list-style-type:none}ul.lst-kix_lrkiroe9ekhf-2{list-style-type:none}.lst-kix_lrkiroe9ekhf-0>li:before{content:"\0025cf   "}ul.lst-kix_lrkiroe9ekhf-3{list-style-type:none}ul.lst-kix_lrkiroe9ekhf-4{list-style-type:none}ul.lst-kix_lrkiroe9ekhf-5{list-style-type:none}ul.lst-kix_lrkiroe9ekhf-6{list-style-type:none}.lst-kix_lrkiroe9ekhf-1>li:before{content:"\0025cb   "}ul.lst-kix_lrkiroe9ekhf-7{list-style-type:none}.lst-kix_3xsvf8xpqkr-4>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-4,lower-latin) ". "}.lst-kix_pa8vl4tnpl8x-0>li:before{content:"\0025cf   "}.lst-kix_pa8vl4tnpl8x-6>li:before{content:"\0025cf   "}.lst-kix_chmeg86wx98z-0>li:before{content:"\0025cf   "}.lst-kix_pa8vl4tnpl8x-8>li:before{content:"\0025a0   "}.lst-kix_q0ktwdf5md65-3>li:before{content:"\0025cf   "}.lst-kix_chmeg86wx98z-6>li:before{content:"\0025cf   "}.lst-kix_q0ktwdf5md65-1>li:before{content:"\0025cb   "}.lst-kix_3xsvf8xpqkr-2>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-2,lower-roman) ". "}ul.lst-kix_72e2zqulhrwf-6{list-style-type:none}ul.lst-kix_72e2zqulhrwf-7{list-style-type:none}ul.lst-kix_72e2zqulhrwf-8{list-style-type:none}ul.lst-kix_72e2zqulhrwf-2{list-style-type:none}ul.lst-kix_72e2zqulhrwf-3{list-style-type:none}ul.lst-kix_72e2zqulhrwf-4{list-style-type:none}.lst-kix_8163nc3u15jq-1>li:before{content:"\0025cb   "}ul.lst-kix_72e2zqulhrwf-5{list-style-type:none}.lst-kix_yztclpytevvw-0>li:before{content:"\0025cf   "}ul.lst-kix_72e2zqulhrwf-0{list-style-type:none}ul.lst-kix_72e2zqulhrwf-1{list-style-type:none}.lst-kix_8163nc3u15jq-3>li:before{content:"\0025cf   "}.lst-kix_72e2zqulhrwf-6>li:before{content:"\0025cf   "}ul.lst-kix_7cx3ikmkibcd-8{list-style-type:none}ul.lst-kix_7cx3ikmkibcd-4{list-style-type:none}ul.lst-kix_7cx3ikmkibcd-5{list-style-type:none}ul.lst-kix_7cx3ikmkibcd-6{list-style-type:none}.lst-kix_72e2zqulhrwf-8>li:before{content:"\0025a0   "}ul.lst-kix_7cx3ikmkibcd-7{list-style-type:none}ul.lst-kix_7cx3ikmkibcd-0{list-style-type:none}ul.lst-kix_7cx3ikmkibcd-1{list-style-type:none}ul.lst-kix_7cx3ikmkibcd-2{list-style-type:none}ul.lst-kix_7cx3ikmkibcd-3{list-style-type:none}.lst-kix_4xenxtb85rpl-1>li:before{content:"\0025cb   "}.lst-kix_28qbb5pba8ll-4>li:before{content:"\0025cb   "}.lst-kix_28qbb5pba8ll-6>li:before{content:"\0025cf   "}ul.lst-kix_oox587co29ny-8{list-style-type:none}ul.lst-kix_oox587co29ny-7{list-style-type:none}.lst-kix_4xenxtb85rpl-7>li:before{content:"\0025cb   "}.lst-kix_72e2zqulhrwf-0>li:before{content:"\0025cf   "}.lst-kix_i9nqtalub2ii-6>li:before{content:"\0025cf   "}.lst-kix_aqvmchp8hu99-3>li:before{content:"\0025cf   "}.lst-kix_i9nqtalub2ii-1>li:before{content:"\0025cb   "}.lst-kix_lenutxuehbqs-8>li:before{content:"\0025a0   "}.lst-kix_ws5to0ylpjnu-1>li:before{content:"\0025cb   "}.lst-kix_aqvmchp8hu99-6>li:before{content:"\0025cf   "}ul.lst-kix_insf2ook9lmq-5{list-style-type:none}ul.lst-kix_xuggaj7hom8a-0{list-style-type:none}ul.lst-kix_insf2ook9lmq-6{list-style-type:none}.lst-kix_ws5to0ylpjnu-4>li:before{content:"\0025cb   "}ul.lst-kix_insf2ook9lmq-7{list-style-type:none}ul.lst-kix_xuggaj7hom8a-2{list-style-type:none}ul.lst-kix_insf2ook9lmq-8{list-style-type:none}ul.lst-kix_xuggaj7hom8a-1{list-style-type:none}ul.lst-kix_insf2ook9lmq-1{list-style-type:none}.lst-kix_wwfczwp99rcu-5>li:before{content:"\0025a0   "}ul.lst-kix_insf2ook9lmq-2{list-style-type:none}.lst-kix_o1xshf1f7b14-4>li:before{content:"\0025cb   "}ul.lst-kix_insf2ook9lmq-3{list-style-type:none}ul.lst-kix_insf2ook9lmq-4{list-style-type:none}.lst-kix_wwfczwp99rcu-8>li:before{content:"\0025a0   "}ul.lst-kix_insf2ook9lmq-0{list-style-type:none}.lst-kix_hy2j2rjtl7zm-2>li:before{content:"\0025a0   "}.lst-kix_rzwdtfa96ijp-3>li:before{content:"\0025cf   "}.lst-kix_nm8cz258lm3y-0>li:before{content:"\0025cf   "}.lst-kix_slhmqripkczd-8>li:before{content:"\0025a0   "}.lst-kix_lenutxuehbqs-0>li:before{content:"\0025cf   "}.lst-kix_urbfmzpl5otu-3>li:before{content:"\0025cf   "}.lst-kix_lenutxuehbqs-3>li:before{content:"\0025cf   "}.lst-kix_wwfczwp99rcu-0>li:before{content:"\0025cf   "}.lst-kix_rzwdtfa96ijp-6>li:before{content:"\0025cf   "}.lst-kix_urbfmzpl5otu-0>li:before{content:"\0025cf   "}.lst-kix_hy2j2rjtl7zm-7>li:before{content:"\0025cb   "}ul.lst-kix_7n6k9dq04clh-8{list-style-type:none}.lst-kix_b5kgyf18mwbc-6>li:before{content:"\0025cf   "}ul.lst-kix_lenutxuehbqs-0{list-style-type:none}ul.lst-kix_7n6k9dq04clh-2{list-style-type:none}.lst-kix_vjixo3ysi0xu-6>li:before{content:"\0025cf   "}ul.lst-kix_7n6k9dq04clh-3{list-style-type:none}ul.lst-kix_7n6k9dq04clh-0{list-style-type:none}ul.lst-kix_7n6k9dq04clh-1{list-style-type:none}ul.lst-kix_7n6k9dq04clh-6{list-style-type:none}ul.lst-kix_7n6k9dq04clh-7{list-style-type:none}.lst-kix_t3aqzvl38zqp-2>li:before{content:"\0025a0   "}ul.lst-kix_7n6k9dq04clh-4{list-style-type:none}.lst-kix_oblnvdf1x5se-5>li:before{content:"\0025a0   "}ul.lst-kix_7n6k9dq04clh-5{list-style-type:none}.lst-kix_t3aqzvl38zqp-7>li:before{content:"\0025cb   "}.lst-kix_vjixo3ysi0xu-1>li:before{content:"\0025cb   "}ul.lst-kix_28qbb5pba8ll-8{list-style-type:none}.lst-kix_v6l0cypl4mld-7>li:before{content:"\0025cb   "}ul.lst-kix_28qbb5pba8ll-6{list-style-type:none}ul.lst-kix_28qbb5pba8ll-7{list-style-type:none}ul.lst-kix_lenutxuehbqs-2{list-style-type:none}ul.lst-kix_28qbb5pba8ll-4{list-style-type:none}ul.lst-kix_lenutxuehbqs-1{list-style-type:none}ul.lst-kix_28qbb5pba8ll-5{list-style-type:none}ul.lst-kix_lenutxuehbqs-4{list-style-type:none}ul.lst-kix_28qbb5pba8ll-2{list-style-type:none}ul.lst-kix_lenutxuehbqs-3{list-style-type:none}.lst-kix_oblnvdf1x5se-2>li:before{content:"\0025a0   "}.lst-kix_urbfmzpl5otu-8>li:before{content:"\0025a0   "}ul.lst-kix_28qbb5pba8ll-3{list-style-type:none}ul.lst-kix_lenutxuehbqs-6{list-style-type:none}ul.lst-kix_28qbb5pba8ll-0{list-style-type:none}ul.lst-kix_lenutxuehbqs-5{list-style-type:none}ul.lst-kix_28qbb5pba8ll-1{list-style-type:none}ul.lst-kix_lenutxuehbqs-8{list-style-type:none}ul.lst-kix_lenutxuehbqs-7{list-style-type:none}.lst-kix_dceblroryw8x-4>li:before{content:"\0025cb   "}ul.lst-kix_o4sb2cmvbb1n-0{list-style-type:none}ul.lst-kix_o4sb2cmvbb1n-1{list-style-type:none}ul.lst-kix_o4sb2cmvbb1n-2{list-style-type:none}ul.lst-kix_o4sb2cmvbb1n-3{list-style-type:none}ul.lst-kix_o4sb2cmvbb1n-4{list-style-type:none}ul.lst-kix_o4sb2cmvbb1n-5{list-style-type:none}.lst-kix_nm8cz258lm3y-5>li:before{content:"\0025a0   "}.lst-kix_7n6k9dq04clh-6>li:before{content:"\0025cf   "}.lst-kix_o1xshf1f7b14-1>li:before{content:"\0025cb   "}ul.lst-kix_aqyufb51wiu2-8{list-style-type:none}ul.lst-kix_aqyufb51wiu2-7{list-style-type:none}.lst-kix_nm8cz258lm3y-8>li:before{content:"\0025a0   "}ul.lst-kix_aqyufb51wiu2-6{list-style-type:none}ul.lst-kix_aqyufb51wiu2-5{list-style-type:none}.lst-kix_dceblroryw8x-1>li:before{content:"\0025cb   "}ul.lst-kix_o4sb2cmvbb1n-6{list-style-type:none}ul.lst-kix_aqyufb51wiu2-4{list-style-type:none}ul.lst-kix_o4sb2cmvbb1n-7{list-style-type:none}ul.lst-kix_aqyufb51wiu2-3{list-style-type:none}ul.lst-kix_o4sb2cmvbb1n-8{list-style-type:none}ul.lst-kix_aqyufb51wiu2-2{list-style-type:none}.lst-kix_7n6k9dq04clh-3>li:before{content:"\0025cf   "}ul.lst-kix_aqyufb51wiu2-1{list-style-type:none}ul.lst-kix_aqyufb51wiu2-0{list-style-type:none}.lst-kix_g6xizdwyjqq3-5>li{counter-increment:lst-ctn-kix_g6xizdwyjqq3-5}.lst-kix_mh8zxn2yduhi-8>li:before{content:"\0025a0   "}ul.lst-kix_rzwdtfa96ijp-7{list-style-type:none}ul.lst-kix_rzwdtfa96ijp-8{list-style-type:none}.lst-kix_pa8vl4tnpl8x-3>li:before{content:"\0025cf   "}ul.lst-kix_rzwdtfa96ijp-5{list-style-type:none}ul.lst-kix_rzwdtfa96ijp-6{list-style-type:none}ul.lst-kix_rzwdtfa96ijp-3{list-style-type:none}.lst-kix_3xsvf8xpqkr-1>li{counter-increment:lst-ctn-kix_3xsvf8xpqkr-1}ul.lst-kix_rzwdtfa96ijp-4{list-style-type:none}ul.lst-kix_rzwdtfa96ijp-1{list-style-type:none}ul.lst-kix_rzwdtfa96ijp-2{list-style-type:none}.lst-kix_3xsvf8xpqkr-7>li:before{content:"" counter(lst-ctn-kix_3xsvf8xpqkr-7,lower-latin) ". "}ul.lst-kix_rzwdtfa96ijp-0{list-style-type:none}.lst-kix_mh8zxn2yduhi-0>li:before{content:"\0025cf   "}.lst-kix_chmeg86wx98z-3>li:before{content:"\0025cf   "}.lst-kix_fhmjbje0v4d4-3>li:before{content:"\0025cf   "}.lst-kix_8163nc3u15jq-6>li:before{content:"\0025cf   "}.lst-kix_o4sb2cmvbb1n-5>li:before{content:"\0025a0   "}.lst-kix_oox587co29ny-4>li:before{content:"\0025cb   "}.lst-kix_flhk8lcnzp86-1>li:before{content:"\0025cb   "}.lst-kix_7cx3ikmkibcd-7>li:before{content:"\0025cb   "}.lst-kix_ow62cky4wecx-5>li:before{content:"\0025a0   "}.lst-kix_72e2zqulhrwf-3>li:before{content:"\0025cf   "}.lst-kix_aqyufb51wiu2-7>li:before{content:"\0025cb   "}.lst-kix_r38jvyodkvi3-3>li:before{content:"\0025cf   "}.lst-kix_28qbb5pba8ll-1>li:before{content:"\0025cb   "}ul.lst-kix_xuggaj7hom8a-8{list-style-type:none}ul.lst-kix_xuggaj7hom8a-7{list-style-type:none}.lst-kix_slhmqripkczd-0>li:before{content:"\0025cf   "}ul.lst-kix_xuggaj7hom8a-4{list-style-type:none}ul.lst-kix_xuggaj7hom8a-3{list-style-type:none}ul.lst-kix_xuggaj7hom8a-6{list-style-type:none}ul.lst-kix_xuggaj7hom8a-5{list-style-type:none}.lst-kix_insf2ook9lmq-1>li:before{content:"\0025cb   "}.lst-kix_cfy6hfjc7ksl-7>li:before{content:"\0025cb   "}.lst-kix_q0ktwdf5md65-6>li:before{content:"\0025cf   "}.lst-kix_4xenxtb85rpl-4>li:before{content:"\0025cb   "}ol{margin:0;padding:0}table td,table th{padding:0}.c4{margin-left:36pt;padding-top:12pt;padding-left:0pt;padding-bottom:12pt;line-height:1.15;orphans:2;widows:2;text-align:left}.c8{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:23pt;font-family:"Arial";font-style:normal}.c0{padding-top:0pt;padding-bottom:0pt;line-height:1.15;orphans:2;widows:2;text-align:left;height:11pt}.c3{color:#000000;font-weight:400;text-decoration:none;vertical-align:baseline;font-size:11pt;font-family:"Arial";font-style:normal}.c2{color:#000000;font-weight:700;text-decoration:none;vertical-align:baseline;font-size:17pt;font-family:"Arial";font-style:normal}.c9{padding-top:24pt;padding-bottom:6pt;line-height:1.15;orphans:2;widows:2;text-align:left}.c1{padding-top:18pt;padding-bottom:4pt;line-height:1.15;orphans:2;widows:2;text-align:left}.c5{padding-top:12pt;padding-bottom:12pt;line-height:1.15;orphans:2;widows:2;text-align:left}.c10{background-color:#ffffff;max-width:451.4pt;padding:72pt 72pt 72pt 72pt}.c6{padding:0;margin:0}.c7{font-style:italic}.title{padding-top:0pt;color:#000000;font-size:26pt;padding-bottom:3pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}.subtitle{padding-top:0pt;color:#666666;font-size:15pt;padding-bottom:16pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}li{color:#000000;font-size:11pt;font-family:"Arial"}p{margin:0;color:#000000;font-size:11pt;font-family:"Arial"}h1{padding-top:20pt;color:#000000;font-size:20pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h2{padding-top:18pt;color:#000000;font-size:16pt;padding-bottom:6pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h3{padding-top:16pt;color:#434343;font-size:14pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h4{padding-top:14pt;color:#666666;font-size:12pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h5{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;orphans:2;widows:2;text-align:left}h6{padding-top:12pt;color:#666666;font-size:11pt;padding-bottom:4pt;font-family:"Arial";line-height:1.15;page-break-after:avoid;font-style:italic;orphans:2;widows:2;text-align:left}</style></head><body class="c10 doc-content"><h1 class="c9" id="h.btvyypbq7s9u"><span class="c8">No Mini-Trial Before Investigation: Supreme Court Clarifies Scope of Magistrate&rsquo;s Power Under Section 175(3) BNSS</span></h1><hr><p class="c0"><span class="c2"></span></p><p class="c5"><span class="c3">In a significant ruling, the Supreme Court has held that High Courts cannot quash a Magistrate&rsquo;s order directing investigation by relying on the defence of the accused. The Court reiterated that such an exercise would amount to conducting a mini-trial at a pre-investigation stage, which is impermissible in law.</span></p><p class="c5"><span class="c3">A Bench comprising Justice Vikram Nath and Justice Sandeep Mehta set aside a Karnataka High Court decision that had interfered with an ongoing investigation after examining defence materials produced by the accused.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.bjg06dtthe2"><span class="c2">Background of the Case</span></h2><p class="c5"><span class="c3">The matter arose from a dispute originating in a civil transaction between the parties, which subsequently took on a criminal dimension. The complainant alleged offences including theft, criminal breach of trust, cheating, forgery, use of forged documents, and criminal conspiracy.</span></p><p class="c5"><span class="c3">At the pre-cognizance stage, the Magistrate exercised powers under Section 156(3) of the Code of Criminal Procedure, 1973, now corresponding to Section 175(3) of the Bharatiya Nagarik Suraksha Sanhita, 2023, and directed the police to register an FIR and conduct an investigation. The Magistrate recorded that the complaint prima facie disclosed the commission of a cognizable offence.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.1ztp45qzjpzh"><span class="c2">High Court&rsquo;s Intervention</span></h2><p class="c5"><span class="c3">The accused approached the Karnataka High Court seeking quashing of the Magistrate&rsquo;s order. The High Court proceeded to examine documents relied upon by the accused, including sale deeds, and treated these materials as determinative of the dispute.</span></p><p class="c5"><span class="c3">It further observed that the complainant ought to have pursued civil remedies, such as cancellation of sale deeds, before initiating criminal proceedings. On this basis, the High Court interfered with the Magistrate&rsquo;s order and effectively stalled the investigation.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.a0e7h8fwmf6m"><span class="c2">Supreme Court&rsquo;s Findings</span></h2><p class="c5"><span class="c3">The Supreme Court found that the High Court had exceeded the permissible limits of its jurisdiction.</span></p><p class="c5"><span class="c3">The Court held that, at the stage of directing investigation under Section 175(3) BNSS (earlier Section 156(3) CrPC), the Magistrate is only required to examine whether the complaint prima facie discloses a cognizable offence. At this stage, the Court must confine itself strictly to the allegations in the complaint and the material placed by the complainant.</span></p><p class="c5"><span class="c3">The Bench observed that the High Court erred in travelling beyond the complaint and examining defence materials produced by the accused. Such an exercise, the Court noted, involves adjudication of disputed questions of fact, which falls within the domain of investigation and, if necessary, trial.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.vccn68pslzqb"><span class="c2">No Consideration of Defence at Threshold Stage</span></h2><p class="c5"><span class="c3">The Court categorically held that the defence of the accused is not relevant at the stage of ordering investigation. Consideration of defence material, including documents such as sale deeds or title records, would amount to conducting a mini-trial at a stage where only a prima facie assessment is required.</span></p><p class="c5"><span class="c3">The Court emphasized that permitting such an approach would defeat the very purpose of directing a police investigation and would undermine the criminal justice process.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.h85fkjnw1ef3"><span class="c2">Limits on High Court&rsquo;s Power Under Section 482 CrPC</span></h2><p class="c5"><span class="c3">The Supreme Court further observed that while exercising inherent powers under Section 482 of the CrPC, High Courts must act with caution and restraint. They cannot:</span></p><ul class="c6 lst-kix_fhmjbje0v4d4-0 start"><li class="c4 li-bullet-0"><span class="c3">Travel beyond the allegations contained in the complaint</span></li><li class="c4 li-bullet-0"><span class="c3">Evaluate defence material produced by the accused</span></li><li class="c4 li-bullet-0"><span class="c3">Conduct a detailed examination of evidence at the threshold stage</span></li></ul><p class="c5"><span class="c3">The Court held that such interference would effectively stifle the investigation at its inception, which is contrary to settled legal principles.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.4iasrh1uwlgn"><span class="c2">Civil Dispute and Criminal Offence</span></h2><p class="c5"><span class="c3">Addressing the High Court&rsquo;s reasoning, the Supreme Court reiterated that the mere existence of a civil remedy does not bar criminal proceedings. Where the allegations in the complaint prima facie disclose the commission of a cognizable offence, criminal law can be set in motion irrespective of parallel civil remedies.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.aj3qlwc6ojwh"><span class="c2">Magistrate&rsquo;s Role Under Section 175(3) BNSS</span></h2><p class="c5"><span class="c3">The Court reaffirmed that the Magistrate&rsquo;s power under Section 175(3) BNSS is exercised at the pre-cognizance stage. The Magistrate is required to:</span></p><ul class="c6 lst-kix_q0ktwdf5md65-0 start"><li class="c4 li-bullet-0"><span class="c3">Apply judicial mind</span></li><li class="c4 li-bullet-0"><span class="c3">Pass a reasoned order</span></li><li class="c4 li-bullet-0"><span class="c3">Be satisfied that the complaint discloses a cognizable offence</span></li><li class="c4 li-bullet-0"><span class="c3">Ensure that procedural requirements, including prior recourse to police authorities, are complied with</span></li></ul><p class="c5"><span class="c3">However, the Magistrate is not required to evaluate the defence of the accused or adjudicate upon disputed facts.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.sjejk33hgjcv"><span class="c2">Reference to Established Judicial Precedents</span></h2><p class="c5"><span class="c3">The judgment is consistent with established jurisprudence governing the scope of investigation and judicial intervention:</span></p><ul class="c6 lst-kix_pa8vl4tnpl8x-0 start"><li class="c4 li-bullet-0"><span>In </span><span class="c7">State of Haryana v. Bhajan Lal</span><span class="c3">&nbsp;(1992), the Supreme Court laid down the limited circumstances under which criminal proceedings may be quashed, emphasizing that such power must be exercised sparingly.</span></li><li class="c4 li-bullet-0"><span>In </span><span class="c7">Priyanka Srivastava v. State of Uttar Pradesh</span><span class="c3">&nbsp;(2015), the Court mandated the filing of a sworn affidavit with applications under Section 156(3) CrPC to prevent misuse of the process, a requirement now incorporated into the BNSS.</span></li><li class="c4 li-bullet-0"><span>In </span><span class="c7">Anil Kumar v. M.K. Aiyappa</span><span class="c3">&nbsp;(2013), the Court emphasized that Magistrates must apply judicial mind before directing investigation and cannot act mechanically.</span></li></ul><p class="c5"><span class="c3">The present ruling builds upon these principles and reaffirms their continued applicability under the BNSS framework.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.yg9lp14fjr4g"><span class="c2">Final Ruling</span></h2><p class="c5"><span class="c3">Allowing the appeal, the Supreme Court set aside the High Court&rsquo;s order and restored the Magistrate&rsquo;s direction for investigation. The Court directed that the investigation proceed from the stage at which it had been interrupted.</span></p><p class="c5"><span class="c3">The Court held that an order directing investigation under Section 175(3) BNSS cannot be quashed by relying on the defence of the accused or materials beyond the complaint.</span></p><hr><p class="c0"><span class="c3"></span></p><h2 class="c1" id="h.pef83c8pqjm6"><span class="c2">Conclusion</span></h2><p class="c5"><span class="c3">This judgment reinforces a fundamental principle of criminal procedure: investigation must precede adjudication. By restricting premature judicial interference and disallowing consideration of defence at the threshold stage, the Supreme Court has preserved the integrity of the investigative process.</span></p><p class="c5"><span class="c3">The ruling ensures that legitimate complaints are not dismissed prematurely and that the criminal justice system functions in accordance with established procedural safeguards.</span></p><p class="c0"><span class="c3"></span></p></body></html>
2. Process 
   a. Scraper the data 
   b. data cleaning 
      i. Remove HTML
      ii. Normalize text 
      iii. Remove ads / noise 
      iv. Standardize format 
   c. Legal relevance filter 
   d. Chunking 
   e. LLM Processing
      i. Classication tags  
      ii. Summary (short 2 lines, detialed)
      iii. Introduction 
      iv. Facts / Background the case of the Law ?
      v. Proceeding history 
         a. Held at lower court and 
         b. Findings 
         c. Consideration 
         d. Limitation  
      iv. Legal Analysis 
          1. What law applies ?
          2. What is legal issue ?
          3. Who is affected ?
          4. Risk involed ?
          5. Previous effect of law ?
          6. Role of the judgement 
      v. Impact analysis 
      vi. Refence to established judicial precedents 
      vii. Finals ruling 
      viii. Final ruling 
      -----<   Input:
    Title: ${article.title}
    Content: ${article.content}
    URL: ${article.url || 'N/A'}
    
    Output Format:
    1. A catchy, professional headline.
    2. A concise executive summary (2-3 sentences).
    3. "Background of the Case" section.
    4. "Key Legal Issues/Findings" section.
    5. "Court's Reasoning" section.
    6. "Significance/Precedents" section (if applicable).
    7. "Final Ruling" section.
    8. A brief conclusion.
    
    Use a professional, neutral tone. Use bullet points for clarity.
    Return the output in Markdown format.>---//Comment 
    Final content types of 
      a. News 
      b. Legal explantion (blogs)
      c. Insight 
      d. newsletter everyday at 8Pm 
      e. Detailed legal research 
-----------------------------------------------------
system Arcchitecture 
🔄 1. FULL LIFECYCLE MANAGEMENT (END-TO-END)

You need 3 parallel lifecycles:

1.1 Data Lifecycle
Ingestion → Validation → Processing → Storage → Usage → Archival → Deletion
Stages:
1. Ingestion
Scraper + APIs
Kafka ingestion
2. Validation
Schema validation (JSON schema)
Deduplication (MinHash)
3. Processing
Cleaning
NLP tagging
LLM transformation
4. Storage
Raw → S3
Processed → PostgreSQL
Search → ElasticSearch
5. Usage
Frontend
APIs
Newsletter
6. Archival
Cold storage (S3 Glacier)
7. Deletion
TTL-based cleanup
GDPR-style compliance ready
1.2 ML Lifecycle (MLOps)
Data → Training → Validation → Deployment → Monitoring → Retraining
Tools:
MLflow
Airflow
Feature Store
Stages:
Data labeling
Model training
Evaluation (accuracy, F1)
Deployment (API)
Monitoring drift
Retraining
1.3 Application Lifecycle (DevOps)
Code → Build → Test → Deploy → Monitor → Scale → Improve
CI/CD:
GitHub Actions
Docker
Kubernetes
🔐 2. SECURITY ARCHITECTURE
2.1 Security Layers
1. Network Security
VPC
Private subnets
API Gateway
2. Application Security
JWT authentication
RBAC (Admin/User roles)
3. Data Security
Encryption at rest (AES-256)
Encryption in transit (TLS 1.3)
4. API Security
Rate limiting (Token Bucket Algorithm)
Input validation
5. Infrastructure Security
IAM roles
Secrets Manager
🔍 3. SECURITY AUDIT SYSTEM
3.1 Automated Security Audit Pipeline
Code Scan → Dependency Scan → API Scan → Infra Scan → Report
3.2 Tools
SAST → Static Code Analysis
DAST → Dynamic Testing
Dependency Scanner → Snyk
3.3 Audit Checks
Code Level
SQL injection
XSS
Hardcoded secrets
API Level
Unauthorized access
Rate abuse
Infra Level
Open ports
Misconfigured IAM
Data Level
PII leakage
Unauthorized access
🤖 4. ML-BASED VULNERABILITY DETECTION SYSTEM

This is where NexLexHub becomes next-level intelligent.

4.1 Goal

👉 Detect + Predict + Fix vulnerabilities automatically

4.2 ML Models Used
1. Anomaly Detection Model
Algorithms:
Isolation Forest
Autoencoders
Use:
Detect unusual API behavior
Detect abnormal traffic
2. Log Classification Model
Algorithms:
BERT / LSTM
Use:
Classify logs:
Normal
Suspicious
Attack
3. Vulnerability Prediction Model
Algorithms:
Random Forest
XGBoost
Input:
Code patterns
Logs
API behavior
4. Graph-Based Attack Detection
Algorithm:
Graph Neural Networks (GNN)
Use:
Detect attack paths
🛠 4.3 Vulnerability Detection Pipeline
Logs → Feature Extraction → ML Model → Risk Score → Alert
⚙️ 5. AUTO-FIX ENGINE (SELF-HEALING SYSTEM)
Mechanism:
Step 1: Detect issue
ML model flags anomaly
Step 2: Classify issue
SQL injection
API abuse
Infra misconfig
Step 3: Apply Fix
Examples:
Issue	Fix
SQL Injection	Add parameterized queries
API abuse	Increase rate limiting
High latency	Scale pods
Step 4: Validate Fix
Re-run tests
Monitor metrics
🔁 6. DEVSECOPS PIPELINE
Pipeline:
Code → Scan → Test → Secure → Deploy → Monitor
Integration Points:
Pre-commit hooks → lint + security
CI → vulnerability scan
CD → secure deployment
📊 7. SECURITY DASHBOARD (ADMIN PANEL)
Features:
1. Threat Monitoring
Active threats
Suspicious activity
2. Risk Scores
System risk level
3. Logs Viewer
Real-time logs
4. Alerts
Email / Slack alerts
5. Auto-Fix Logs
What was fixed automatically
📈 8. PERFORMANCE + SECURITY METRICS
Track:
Metric	Description
Error Rate	% failed requests
Latency	API response time
Threat Count	Security incidents
QA Score	Content quality
Model Accuracy	ML performance
🧠 9. ADVANCED ALGORITHMS USED
Function	Algorithm
Crawling	BFS
Deduplication	MinHash
Classification	BERT
Chunking	Sliding Window
Similarity	Cosine Similarity
Search	BM25
Recommendation	Content Filtering
Rate limiting	Token Bucket
Retry	Exponential Backoff
Anomaly Detection	Isolation Forest
Attack Detection	GNN
🔥 10. FINAL SECURE SYSTEM FLOW
Scraper
 ↓
Kafka
 ↓
Processing + NLP
 ↓
LLM Engine
 ↓
QA Engine
 ↓
Security Scan (ML)
 ↓
Storage
 ↓
Frontend
 ↓
User
🧠 FINAL INSIGHT

With this addition, NexLexHub becomes:

👉 Self-learning + Self-healing + Secure Legal AI Platform
** core components 
| Layer     | Purpose               |
| --------- | --------------------- |
| Scraper   | Collect data          |
| Pipeline  | Clean & process       |
| AI Engine | Generate insights     |
| QA Engine | Validate accuracy     |
| Storage   | Store structured data |
| API       | Serve data            |
| Frontend  | Display               |
| Dashboard | Control system        |
-----------------------------------------------------
3. Data Pipeline 
   3.1 - Live law 
   3.2 - Bar and Bench
   3.3 - ET Legal worlds
   3.4 - Google news 
   3.5 - Other sources 
   
   3.A - Pipeline flow "Scraper → Cleaning → Filtering → Chunking → LLM → QA → Storage"

   🧠 1. OVERVIEW — WHAT THIS SYSTEM REALLY IS

At its core, NexLexHub Phase 1 is a distributed AI pipeline system that:

Collects legal data
Cleans and structures it
Applies ML + LLM reasoning
Validates output quality
Publishes high-quality legal intelligence

This is not a simple pipeline — it is:

A combination of Data Engineering + NLP + Distributed Systems + DevSecOps

🔄 2. PIPELINE STAGES (DETAILED ENGINEERING VIEW)
🔍 A. SCRAPER LAYER
🎯 Purpose

To continuously fetch legal news from multiple sources efficiently and without duplication.

⚙️ Tech Stack
Python
BeautifulSoup → static scraping
Playwright → dynamic scraping
🧠 Algorithms Used
1. Breadth-First Search (BFS)

Used to crawl:

Pagination pages
Category pages
Why BFS?
Ensures latest content first
Avoids deep crawling loops
2. Queue (FIFO Data Structure)

Used for:

URL management
queue = deque(start_urls)
3. HashSet (Set DS)

Used for:

Deduplication
if url not in visited:
🧱 Internal Architecture
[Seed URLs]
   ↓
[Queue]
   ↓
[Scraper Workers]
   ↓
[Visited Set Check]
   ↓
[Extract Content]
⚡ Optimization Techniques
Parallel scraping (multi-threading)
Rate limiting (Token Bucket Algorithm)
Retry (Exponential Backoff)
🧹 B. DATA CLEANING LAYER
🎯 Purpose

Convert messy HTML into clean, structured legal text

Steps:
Remove HTML tags
Normalize text
Remove ads/noise
Standardize format
🧠 Algorithms
1. Regex Parsing
Remove scripts, ads
2. Tokenization
Split into sentences/words
3. Stopword Removal
DSA Used
String manipulation
Arrays (token lists)
Pipeline:
Raw HTML → Regex → Clean Text → Tokenization → Output
⚖️ C. LEGAL RELEVANCE FILTER
🎯 Purpose

Filter only legal content

Model:
Legal-BERT
Input:
Article text
Output:
{
  "is_legal": true,
  "category": "Criminal"
}
🧠 Algorithm
Transformer-based Classification
Attention mechanism
Context-aware classification
DSA Used
Vectors (embeddings)
Matrices (attention computation)
✂️ D. CHUNKING ENGINE
🎯 Purpose

Break large content for LLM processing

Algorithms:
1. Sliding Window Algorithm
for i in range(0, len(text), chunk_size):
2. Greedy Chunking
Max tokens per chunk
Why Needed?
LLM token limits
Context preservation
DSA Used
Arrays
Iteration
🤖 E. LLM PROCESSING ENGINE
🎯 Purpose

Convert raw legal content into structured legal knowledge

Outputs:
Summary
Background
Legal Issues
Court reasoning
Precedents
Final ruling
🧠 Algorithms / Techniques
1. Prompt Engineering
Structured prompts
2. Few-shot Learning
Example-based learning
3. Chain-of-Thought (CoT)
Step-by-step reasoning
Internal Flow:
Chunk → Prompt → LLM → Structured Output
🧪 F. QA ENGINE
🎯 Purpose

Ensure:

Accuracy
Completeness
No hallucination
Layers:
1. Structural Validation

Check:

Missing sections
2. Accuracy Validation

Compare:

Source vs generated
3. Hallucination Detection
Algorithm:
Cosine Similarity
Similarity = cosine(embedding1, embedding2)
4. Scoring System
Weighted Score
Final Score = w1*A + w2*R + w3*C + w4*Cl + w5*Ct
DSA Used
Vectors
Arrays
HashMaps
🧪 4. QUALITY SYSTEM (DETAILED)
Metrics:
Metric	Meaning
Accuracy	Correctness
Relevance	Legal alignment
Completeness	Coverage
Clarity	Readability
Citations	Reference validity
Publishing Logic:
Score < 7 → Reject  
Score 7–8 → Manual review  
Score > 8 → Auto publish  
🤖 5. AI & ML SYSTEM
Models:
Model	Use
BERT	Classification
GPT/T5	Summarization
Sentence Transformer	Embeddings
Isolation Forest	Security
ML Pipeline:
Data → Train → Evaluate → Deploy → Monitor → Retrain
Feature Store:

Stores:

Embeddings
Tags
Outputs
🧠 6. ALGORITHMS (FULL SYSTEM)
Task	Algorithm
Crawling	BFS
Deduplication	MinHash
Classification	BERT
Chunking	Sliding Window
Similarity	Cosine Similarity
Search	BM25
Rate limit	Token Bucket
Retry	Exponential Backoff
Security	Isolation Forest
📦 7. DATA STORAGE DESIGN
PostgreSQL

Stores:

Articles
Tags
Logs
ElasticSearch
Full-text search
Inverted index
S3
Raw HTML
JSON
Vector DB
Embeddings
Semantic search
🔄 8. CRUD OPERATIONS
APIs:
POST → create
GET → read
PUT → update
DELETE → delete
DSA Used
HashMaps (fast lookup)
Indexing
🎨 9. FRONTEND SYSTEM
Tech:
Next.js
Tailwind
Pages:
Home
Trending news
Article Page
Structured legal data
Search Page
Filters
Admin Dashboard
System control
📊 10. ADMIN DASHBOARD
Modules:
Content monitoring
Pipeline monitoring
QA scores
Logs
Automation
DSA Used:
Graphs (pipeline visualization)
Queues (job tracking)
🔁 11. EVENT-DRIVEN SYSTEM
Kafka Topics:
raw_articles
processed_articles
failed_jobs
DSA:
Queue-based messaging
🔐 12. SECURITY SYSTEM
Layers:
JWT
RBAC
Encryption
Rate limiting
Algorithms:
Token Bucket
Hashing
🔍 13. SECURITY AUDIT
Pipeline:
Code → API → Infra → Report
Checks:
SQL injection
XSS
Misconfig
🤖 14. ML VULNERABILITY SYSTEM
Models:
Isolation Forest
Random Forest
BERT
Flow:
Logs → Features → Model → Risk Score
🛠 15. AUTO-FIX SYSTEM
Examples:
Issue	Fix
API abuse	Rate limit
SQL injection	Safe queries
Load spike	Scale
🔄 16. LIFECYCLE MANAGEMENT
Data Lifecycle:
Ingest → Process → Store → Archive
ML Lifecycle:
Train → Deploy → Monitor
App Lifecycle:
Build → Deploy → Improve
🔁 17. CI/CD PIPELINE
CI:
Lint
Test
CD:
Deploy
Monitor
🧪 18. TESTING STRATEGY
Unit tests
Integration tests
AI validation
Data testing
🧰 19. INFRASTRUCTURE
Tools:
Docker
Kubernetes
Terraform
📊 20. PERFORMANCE METRICS

Track:

Articles/day
Latency
Errors
QA score
🎯 21. FINAL EXECUTION FLOW
Scrape → Clean → Filter → Chunk → LLM → QA → Store → Publish → Monitor