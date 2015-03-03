<%inherit file="base.mako"/>
<%def name="title()">FAQ</%def>
<%def name="content()">
<h1 class="page-title">Frequently Asked Questions</h1>
<h3>How much does the OSF service cost?</h3><p>It's free!</p>

<h3>How can it be free? How are you funded?</h3><p>OSF is
    maintained and developed by the Center for Open Science (COS), a non-profit
    organization. COS is supported through grants from a variety of supporters,
    including <a href="http://centerforopenscience.org/about_sponsors/">
    federal agencies, private foundations, and commercial entities</a>.</p>

<h3>How will the OSF be useful to my research?</h3><p>The OSF integrates with
    the scientist's daily workflow. OSF helps document and archive study
    designs, materials, and data. OSF facilitates sharing of materials and data
    within a laboratory or across laboratories. OSF also facilitates transparency of
    laboratory research and provides a network design that details and credits
    individual contributions for all aspects of the research process. To see how
    it works, watch our short <a
            href="/getting-started">Getting
        Started</a> videos, see the <a
            href="/4znZP/wiki/home">OSF
        Features </a>page, or see how other scientists <a href="/svje2/">use the OSF.</a></p>

<h3>How can I use the OSF?</h3><p>OSF membership is open and free, so you can
    just register and get started!</p>

<h3>What if I don't want to make anything available publicly in the OSF?</h3><p>
    The OSF is designed to support both private and public workflows. You can
    keep projects, or individual components of projects, private so that only
    your project collaborators have access to them.</p>

<h3>What is a registration?</h3><p>A registration certifies what was done in
    advance of data analysis or confirms the exact state of the project at
    important points of the lifecycle, such as manuscript submission or the
    onset of data collection.</p>

<h3>Do registrations have to be public?</h3><p>No. Registration can occur
    privately. Others could only know that a registration has occurred, but not
    what was registered. The most common use case of private registration is to
    keep a research design private before data collection is complete.</p>

<h3>What if I don't want to register anything in the OSF?</h3><p>Registering is
    an optional feature of the OSF.</p>

<h3>How secure is my information?</h3><p>Security is extremely important for
    the OSF. When you sign up and create a password, your password is not
    recorded. Instead, we store a <a href="http://bcrypt.sourceforge.net/">bcrypt
        hash</a> of your password. This is a computation on your password that
    cannot be reversed, but is the same every time it is computed from your
    password. This provides extra security. No one but you can know your
    password. When you click "Forgot your password," OSF sends you a new random
    password because it neither stores nor has the ability to compute your password.</p>

<p>Data and materials posted on OSF are not yet encrypted, unless you encrypt
    them before uploading to the site. This means that if our servers were
    compromised, the intruder would have access to raw data. While we have taken
    technological measures to minimize this risk, the level of security can be
    improved further. We will offer encryption soon, and we will partner with
    data storage services that offer strong security features.</p>

<h3>How does OSF store and back up files that I upload to the site?</h3>
    <p>The OSF stores files with <a href="http://www.rackspace.com/">Rackspace</a>
    via an open source sponsorship, and has backups on 
    <a href="http://aws.amazon.com/glacier/">Amazon's Glacier platform</a>. 
    OSF maintains several backup schemes, including off-site backups and 
    automated backups performed by our host every day, week, and fortnight.</p>

<h3>What is coming to the OSF?</h3>

<p>The OSF infrastructure will be open-sourced to encourage a community of
    developers to contribute to open science by adding features and improving
    existing features. For updates on new features, you can join our <a href="https://groups.google.com/forum/#!forum/openscienceframework">Google
        Group</a>, find us on <a
            href="https://twitter.com/osframework">Twitter</a> and on <a
            href="https://www.facebook.com/OpenScienceFramework">Facebook</a>,
    or follow the COS <a
            href="https://github.com/centerforopenscience">GitHub</a> page.</p>
<h3>How can I help develop the OSF?</h3><p>If you are a developer, email the <a
        href="mailto:contact@osf.io">dev team</a> for
    more information. If you want to comment on how to make the OSF more useful
    for managing your workflow, send comments <a
            href="mailto:contact@osf.io">here</a>.</p>
</%def>
