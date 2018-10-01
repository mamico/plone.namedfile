# -*- coding: utf-8 -*-
from plone.testing import Layer
from plone.testing import publisher
from plone.testing import zca
from plone.testing import zodb
from plone.testing import zope
from zope.configuration import xmlconfig


class NamedFileTestLayer(Layer):

    defaultBases = (zope.STARTUP, publisher.PUBLISHER_DIRECTIVES)

    def setUp(self):
        zca.pushGlobalRegistry()

        import plone.namedfile
        xmlconfig.file('testing.zcml', plone.namedfile)

    def testSetUp(self):
        self['zodbDB_before_namedfile'] = self.get('zodbDB')
        self['zodbDB'] = zodb.stackDemoStorage(
            self.get('zodbDB'),
            name='NamedFileFixture'
        )

    def tearDown(self):
        # Zap the stacked zca context
        zca.popGlobalRegistry()

    def testTearDown(self):
        # Zap the stacked ZODB
        self['zodbDB'].close()
        self['zodbDB'] = self['zodbDB_before_namedfile']
        del self['zodbDB_before_namedfile']


PLONE_NAMEDFILE_FIXTURE = NamedFileTestLayer()

PLONE_NAMEDFILE_INTEGRATION_TESTING = zope.IntegrationTesting(
    bases=(PLONE_NAMEDFILE_FIXTURE, ),
    name='plone.namedfile:NamedFileTestLayerIntegration',
)

PLONE_NAMEDFILE_FUNCTIONAL_TESTING = zope.FunctionalTesting(
    bases=(PLONE_NAMEDFILE_FIXTURE, ),
    name='plone.namedfile:NamedFileTestLayerFunctional',
)
